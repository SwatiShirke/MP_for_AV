// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from vd_msgs:msg/VDControlCMD.idl
// generated code does not contain a copyright notice

#ifndef VD_MSGS__MSG__DETAIL__VD_CONTROL_CMD__TRAITS_HPP_
#define VD_MSGS__MSG__DETAIL__VD_CONTROL_CMD__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "vd_msgs/msg/detail/vd_control_cmd__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace vd_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const VDControlCMD & msg,
  std::ostream & out)
{
  out << "{";
  // member: velocity
  {
    out << "velocity: ";
    rosidl_generator_traits::value_to_yaml(msg.velocity, out);
    out << ", ";
  }

  // member: steering_angle
  {
    out << "steering_angle: ";
    rosidl_generator_traits::value_to_yaml(msg.steering_angle, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const VDControlCMD & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: velocity
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "velocity: ";
    rosidl_generator_traits::value_to_yaml(msg.velocity, out);
    out << "\n";
  }

  // member: steering_angle
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "steering_angle: ";
    rosidl_generator_traits::value_to_yaml(msg.steering_angle, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const VDControlCMD & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace vd_msgs

namespace rosidl_generator_traits
{

[[deprecated("use vd_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const vd_msgs::msg::VDControlCMD & msg,
  std::ostream & out, size_t indentation = 0)
{
  vd_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use vd_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const vd_msgs::msg::VDControlCMD & msg)
{
  return vd_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<vd_msgs::msg::VDControlCMD>()
{
  return "vd_msgs::msg::VDControlCMD";
}

template<>
inline const char * name<vd_msgs::msg::VDControlCMD>()
{
  return "vd_msgs/msg/VDControlCMD";
}

template<>
struct has_fixed_size<vd_msgs::msg::VDControlCMD>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<vd_msgs::msg::VDControlCMD>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<vd_msgs::msg::VDControlCMD>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // VD_MSGS__MSG__DETAIL__VD_CONTROL_CMD__TRAITS_HPP_
