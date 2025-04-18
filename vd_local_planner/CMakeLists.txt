cmake_minimum_required(VERSION 3.8)
project(vd_local_planner)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(Eigen3 REQUIRED)
find_package(yaml-cpp REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(rclcpp_components REQUIRED)
find_package(carla_msgs REQUIRED)
find_package(vd_msgs REQUIRED)
find_package(casadi REQUIRED)



# ARM NEON flags
if ("${CMAKE_HOST_SYSTEM_PROCESSOR}" STREQUAL "armv7l")
  set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -march=armv7-a -mfpu=neon -mfloat-abi=hard -funsafe-math-optimizations")
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -march=armv7-a -mfpu=neon -mfloat-abi=hard -funsafe-math-optimizations")
  message("enabling ARM neon optimizations")
endif()

# flags for speed (should already be enabled by default)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra")
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -g")
set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -fopenmp -O3")

# Set the acados source path from bashrc

set(acados_path "/home/swati/acados")
set(acados_lib ${acados_path}/lib) 
set(casadi_lib_path "$ENV{HOME}/.casadi_cpp/lib")
set(casadi_include_path "$ENV{HOME}/.casadi_cpp/include")
set(hsl_path "/opt/hsl/ma27")
set(ipopt_include_path "/usr/local/include/coin-or")
set(ipopt_lib_path /usr/local/lib)



#set all paths for req libs so  and include
set(acados_generated_code "scripts/c_generated_code")
set(cbf_solver_lib_path ${CMAKE_CURRENT_SOURCE_DIR}/scripts)



set(dependencies
  rclcpp
  geometry_msgs
  vd_msgs
  nav_msgs
  std_msgs
  sensor_msgs
  Eigen3
  yaml-cpp
  tf2
  tf2_ros
  rclcpp_components
  carla_msgs
)

include_directories(
  "include"
  ${EIGEN3_INCLUDE_DIR}
  ${acados_generated_code}
  ${acados_path}
  ${acados_path}/interfaces
  ${acados_path}/acados
  ${acados_path}/acados/utils
  ${acados_path}/external
  ${acados_path}/external/blasfeo/include
  ${acados_path}/external/hpipm/include
  ${casadi_include_path}
  ${ipopt_include_path}
 
)


link_directories(${acados_generated_code})
add_library(nmpc_shared_lib SHARED src/nmpc_control_node.cpp src/wrapper.cpp src/nmpc_control.cpp src/cbf_solver.cpp )
set_target_properties(nmpc_shared_lib PROPERTIES COMPILE_DEFINITIONS "COMPOSITION_BUILDING_DLL")
ament_target_dependencies(nmpc_shared_lib ${dependencies})

#include .so files
install( FILES scripts/c_generated_code/libacados_ocp_solver_ackerman_model.so
DESTINATION lib
)

install(FILES scripts/libcbf_solver.so DESTINATION lib)


target_link_libraries(nmpc_shared_lib  
  libacados_ocp_solver_ackerman_model.so
  ${YAML_CPP_LIBRARIES}  
  ${acados_lib}/libacados.so
  ${casadi_lib_path}/libcasadi.so
  ${ipopt_lib_path}/libipopt.so
  ${hsl_path}/libhsl.so    
  ${cbf_solver_lib_path}/libcbf_solver.so 
)

#rclcpp_components_register_nodes(nmpc_shared_lib "nmpc_control_nodelet::NMPCControlNodelet")
ament_export_libraries(nmpc_shared_lib)
ament_export_dependencies(${dependencies})

add_executable(vd_nmpc_node src/nmpc_control_node.cpp)
ament_target_dependencies(vd_nmpc_node ${dependencies})
target_link_libraries(vd_nmpc_node nmpc_shared_lib 

 )

# Install targets
install(TARGETS  
  vd_nmpc_node
  DESTINATION lib/${PROJECT_NAME}
)


install( TARGETS
  nmpc_shared_lib
  ARCHIVE DESTINATION lib/${PROJECT_NAME}
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin

)

# Install include directory
install(DIRECTORY include/
  DESTINATION include/
)


if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()

