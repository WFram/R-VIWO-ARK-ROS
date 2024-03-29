cmake_minimum_required(VERSION 2.4.6)
project(r_viwo_ark)

#include($ENV{ROS_ROOT}/core/rosbuild/rosbuild.cmake)

#rosbuild_init()

add_definitions(-std=c++14)

#IF(NOT ROS_BUILD_TYPE)
#    SET(ROS_BUILD_TYPE Release)
#ENDIF()

#LIST(APPEND CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/R-VIWO-ARK-ROS/cmake)

#MESSAGE("Build type: " ${ROS_BUILD_TYPE})

LIST(APPEND CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/R-VIWO-ARK/cmake_modules)

find_package(catkin REQUIRED COMPONENTS
        rosbag
        roscpp
        std_msgs
        cv_bridge
        image_transport
        tf
        tf2_geometry_msgs
        tf2_ros
        sensor_msgs
        message_generation)

find_package(OpenCV 4 REQUIRED)
if (NOT OpenCV_FOUND)
    message(FATAL_ERROR "OpenCV > 4.4 not found.")
endif ()

find_package(Eigen3 3.1.0 REQUIRED)
#find_package(Sophus REQUIRED)
find_package(Pangolin REQUIRED)

#find_package(DBoW2 REQUIRED)
#if (DBoW2_FOUND)
#    MESSAGE("DBOW2 at: " ${dbow2_catkin_INCLUDE_DIRS})
#    MESSAGE("DBOW2 Libs at: " ${dbow2_catkin_LIBRARIES})
#endif ()

#find_package(g2o REQUIRED)
#if (g2o_FOUND)
#    MESSAGE("g2o at: " ${g2o_INCLUDE_DIRS})
#    MESSAGE("g2o Libs at: " ${g2o_LIBRARIES})
#endif ()

find_package(TBB REQUIRED)
message(STATUS "Found TBB ${TBB_VERSION_MAJOR}.${TBB_VERSION_MINOR} (interface version ${TBB_INTERFACE_VERSION}) headers in: ${TBB_INCLUDE_DIRS}")
if (TBB_INTERFACE_VERSION LESS 11004)
    # enable global_control header for earlier TBB versions (Ubuntu 16.04, 18.04)
    add_definitions(-DTBB_PREVIEW_GLOBAL_CONTROL)
endif ()
set(LIBS_ROS
        ${PROJECT_SOURCE_DIR}/R-VIWO-ARK/Thirdparty/DBoW2/lib/libDBoW2.so
        ${PROJECT_SOURCE_DIR}/R-VIWO-ARK/Thirdparty/g2o/lib/libg2o.so
        ${PROJECT_SOURCE_DIR}/R-VIWO-ARK/lib/libR-VIWO-ARK.so
        ${OpenCV_LIBS}
        ${catkin_LIBRARIES}
#        ${Sophus_LIBRARIES}
        -lboost_system
        -lcrypto
        ${Pangolin_LIBRARIES}
        ${TBB_LIBRARIES}
        )

catkin_package(
        CATKIN_DEPENDS roscpp rospy std_msgs cv_bridge image_transport tf sensor_msgs message_runtime
        LIBRARIES ${PROJECT_NAME}
)
add_library(${PROJECT_NAME} SHARED
        R-VIWO-ARK-ROS/src/utils/Utils.cpp
        R-VIWO-ARK-ROS/include/utils/Utils.h
        )
target_link_libraries(${PROJECT_NAME}
        ${LIBS_ROS}
        )
include_directories(
        ${catkin_INCLUDE_DIRS}
        ${PROJECT_SOURCE_DIR}/R-VIWO-ARK/Thirdparty/Sophus
        ${PROJECT_SOURCE_DIR}/R-VIWO-ARK
        ${PROJECT_SOURCE_DIR}/R-VIWO-ARK/include
        ${PROJECT_SOURCE_DIR}/R-VIWO-ARK/include/CameraModels
        ${PROJECT_SOURCE_DIR}/R-VIWO-ARK-ROS
        ${PROJECT_SOURCE_DIR}/R-VIWO-ARK-ROS/include
        ${PROJECT_SOURCE_DIR}/R-VIWO-ARK-ROS/include/Utils
#        ${g2o_INCLUDE_DIR}
#        ${DBoW2_INCLUDE_DIR} # TODO: Maybe need to set them
        ${Pangolin_INCLUDE_DIRS}
        ${TBB_INCLUDE_DIR}
)

add_executable(${PROJECT_NAME}_rgbd_semantic
        R-VIWO-ARK-ROS/src/ros_rgbd_semantic.cc
        R-VIWO-ARK-ROS/src/node.cpp R-VIWO-ARK-ROS/include/node.h)

target_link_libraries(${PROJECT_NAME}_rgbd_semantic
        ${LIBS_ROS}
        ${PROJECT_NAME}
        )

#add_executable(${PROJECT_NAME}_stereo_inertial
#        ORB_SLAM3_ROS/src/ros_stereo_inertial.cc
#        ORB_SLAM3_ROS/src/node.cpp ORB_SLAM3_ROS/include/node.h)

#target_link_libraries(${PROJECT_NAME}_stereo_inertial
#        ${LIBS_ROS}
#        ${PROJECT_NAME}
#        )
#add_executable(${PROJECT_NAME}_stereo_inertial_new
#        ORB_SLAM3_ROS/src/ros_stereo_inertial_new.cpp
#        ORB_SLAM3_ROS/src/node.cpp ORB_SLAM3_ROS/include/node.h)
#
#target_link_libraries(${PROJECT_NAME}_stereo_inertial_new
#        ${LIBS_ROS}
#        ${PROJECT_NAME}
#        )
#add_executable(${PROJECT_NAME}_stereo
#        ORB_SLAM3_ROS/src/ros_stereo.cc
#        ORB_SLAM3_ROS/src/node.cpp ORB_SLAM3_ROS/include/node.h)
#
#target_link_libraries(${PROJECT_NAME}_stereo
#        ${LIBS_ROS}
#        ${PROJECT_NAME}
#        )
#add_executable(${PROJECT_NAME}_stereo_offline
#        ORB_SLAM3_ROS/src/ros_stereo_offline.cc
#        ORB_SLAM3_ROS/src/node.cpp ORB_SLAM3_ROS/include/node.h)
#
#target_link_libraries(${PROJECT_NAME}_stereo_offline
#        ${LIBS_ROS}
#        ${PROJECT_NAME}
#        )
