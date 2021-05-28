
cmake_minimum_required(VERSION 3.5)
project(actor_plugin)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

find_package(actor_services REQUIRED)
find_package(tf2_ros REQUIRED)

include_directories(include ${roscpp_INCLUDE_DIRS})
include_directories(include ${actor_services_INCLUDE_DIRS})
include_directories(include ${tf_INCLUDE_DIRS})
include_directories(include ${std_msgs_INCLUDE_DIRS})
include_directories(include /user/include/sdformat-5.2)
include_directories(include ./include)
find_package(gazebo REQUIRED)
include_directories(include ${GAZEBO_INCLUDE_DIRS})
link_directories(${GAZEBO_LIBRARY_DIRS})
list(APPEND CMAKE_CXX_FLAGS "${GAZEBO_CXX_FLAGS}")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${GAZEBO_CXX_FLAGS}")

add_library(actorplugin_ros SHARED src/ActorPlugin_ros.cc)
target_link_libraries(actorplugin_ros ${GAZEBO_LIBRARIES} ${tf_LIBRARIES})#target_link_libraries or ament_target_dependencies?

ament_target_dependencies(actorplugin_ros
  rclcpp
  std_msgs)

set_target_properties(actorplugin_ros PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/lib)

install(DIRECTORY include/
  DESTINATION include)
ament_export_include_directories(include)
ament_export_dependencies(std_msgs)
ament_package()
#catkin_ament_package()