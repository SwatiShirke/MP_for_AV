// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__rosidl_typesupport_fastrtps_cpp.hpp.em
// with input from vd_msgs:msg/VDpose.idl
// generated code does not contain a copyright notice

#ifndef VD_MSGS__MSG__DETAIL__V_DPOSE__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
#define VD_MSGS__MSG__DETAIL__V_DPOSE__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "vd_msgs/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
#include "vd_msgs/msg/detail/v_dpose__struct.hpp"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

#include "fastcdr/Cdr.h"

namespace vd_msgs
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_vd_msgs
cdr_serialize(
  const vd_msgs::msg::VDpose & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_vd_msgs
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  vd_msgs::msg::VDpose & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_vd_msgs
get_serialized_size(
  const vd_msgs::msg::VDpose & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_vd_msgs
max_serialized_size_VDpose(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace vd_msgs

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_vd_msgs
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, vd_msgs, msg, VDpose)();

#ifdef __cplusplus
}
#endif

#endif  // VD_MSGS__MSG__DETAIL__V_DPOSE__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
