//
// Created by wfram on 3/31/22.
//

#ifndef R_VIWO_ARK_WS_UTILS_H
#define R_VIWO_ARK_WS_UTILS_H

// From R-VIWO-ARK
#include <MapPoint.h>

// From ROS
#include <sensor_msgs/PointCloud2.h>
#include <tf2_geometry_msgs/tf2_geometry_msgs.h>

// From Sophus
#include <sophus/se3.hpp>

namespace Utils {

    void toTransformMsg(Sophus::SE3f Twc, geometry_msgs::Transform* tf);
    ros::Time toROSTime(double timestamp);
//void TftoTarget()
};

#endif //R_VIWO_ARK_WS_UTILS_H
