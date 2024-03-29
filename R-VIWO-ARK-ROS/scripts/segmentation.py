#!/usr/bin/env python3

import sys
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from std_msgs.msg import Header
import cv2
import re
import numpy as np
from mmseg.apis import inference_segmentor, init_segmentor
import mmcv
import message_filters

class Segmenter(object):
    def __init__(self, topic_kf, topic_in, topic_out):
        self.cv_bridge = CvBridge()
        rospy.loginfo("Segmentation  " + topic_in + "output topic: " + topic_out)
        #self.config_file = '/home/ami/slam_ws/SeMask-Segmentation/SeMask-FPN/configs/semask_swin/ade20k/semfpn_semask_swin_base_patch4_window12_512x512_80k_ade20k.py'
        #self.checkpoint_file = '/home/ami/slam_ws/SeMask-Segmentation/semask_base_fpn_ade20k.pth'

        self.config_file = '/home/wfram/mmsegmentation/configs/pspnet/pspnet_r101-d8_512x512_80k_ade20k.py'
        self.checkpoint_file = '/home/wfram/Downloads/pspnet_r101-d8_512x512_80k_ade20k_20200614_031423-b6e782f0.pth'
        self.model = init_segmentor(self.config_file, self.checkpoint_file, device='cuda:0')
        self.palette = np.array(self.model.PALETTE)
        #self.palette = np.array(self.palette)
        self.width = 640
        self.height = 480
        self.frame = None
        self.stamp = None
        self.kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))

        self.pub = rospy.Publisher(topic_out, Image, queue_size=1)

        #self.sub = rospy.Subscriber(topic_in, Image, self.image_rec, queue_size=1)
        rospy.loginfo("Starting to handle")
        self.sub_orig = message_filters.Subscriber(topic_in, Image, queue_size=5)
        self.sub_kf = message_filters.Subscriber(topic_kf, Image, queue_size=5)
        self.ts = message_filters.ApproximateTimeSynchronizer([self.sub_orig, self.sub_kf], 10, 0.1, allow_headerless=True)
        self.ts.registerCallback(self.image_rec)

        self.idx=0
    def publish(self, result, frame_id, stamp_now):
        result = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
        img_msg = self.cv_bridge.cv2_to_imgmsg(result, encoding='rgb8')
        #img_msg.header = self.header
        img_msg.header.frame_id = frame_id
        img_msg.header.stamp = stamp_now
        self.pub.publish(img_msg)

    def segment(self, img):
        img = img[:, :, :3]
        img_orig = img.copy()
        img = cv2.resize(img, (0, 0), fx=0.35, fy=0.35, interpolation=cv2.INTER_AREA)
        #img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        result = inference_segmentor(self.model, img)
        #img = mmcv.imread(img)
        #img = img.copy()
        #h, w = img.shape[:2]
        seg = result[0][0]
        color_seg = np.zeros((seg.shape[0], seg.shape[1], 3), dtype=np.uint8)
        for label, color in enumerate(self.palette):
            color_seg[seg == label, :] = color
        color_seg = color_seg[..., ::-1]
        color_seg = mmcv.imresize(color_seg, (self.width, self.height), interpolation='nearest', backend='cv2')
        color_seg = color_seg * 0.7 + img_orig * 0.3
        self.pred = color_seg.astype(np.uint8)
        #self.pred = cv2.morphologyEx(self.pred, cv2.MORPH_OPEN, self.kernel)
        self.publish(self.pred, self.frame, self.stamp)

    def image_rec(self, msg1, msg2):
        self.idx = self.idx + 1
        #rospy.loginfo("Received image " + str(self.idx))
        #self.header = Header(stamp=msg2.header.stamp)
        self.frame = msg2.header.frame_id
        self.stamp = msg2.header.stamp
        self.image_input = self.cv_bridge.imgmsg_to_cv2(msg1)
        self.segment(self.image_input)


if __name__ == '__main__':
    #argv = rospy.myargv(sys.argv)
    rospy.init_node("segmentation", anonymous=True, log_level=rospy.DEBUG)
    kf = rospy.get_param('~input_topic')
    #kf = '/vslam_stereo_inertial/KF_DebugImage'
    input_ori = rospy.get_param('~image_input_original_topic')
    #input_ori = '/zed2/zed_node/left/image_rect_color'

    output_semantic = rospy.get_param('~segmentation_topic')
    #output_semantic = '/zed2/zed_node/semantics'
    seg = Segmenter(kf, input_ori, output_semantic)
    rospy.spin()