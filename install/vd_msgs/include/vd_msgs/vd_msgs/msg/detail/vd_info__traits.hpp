// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from vd_msgs:msg/VDInfo.idl
// generated code does not contain a copyright notice

#ifndef VD_MSGS__MSG__DETAIL__VD_INFO__TRAITS_HPP_
#define VD_MSGS__MSG__DETAIL__VD_INFO__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "vd_msgs/msg/detail/vd_info__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace vd_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const VDInfo & msg,
  std::ostream & out)
{
  out << "{";
  // member: x
  {
    out << "x: ";
    rosidl_generator_traits::value_to_yaml(msg.x, out);
    out << ", ";
  }

  // member: y
  {
    out << "y: ";
    rosidl_generator_traits::value_to_yaml(msg.y, out);
    out << ", ";
  }

  // member: yaw
  {
    out << "yaw: ";
    rosidl_generator_traits::value_to_yaml(msg.yaw, out);
    out << ", ";
  }

  // member: length
  {
    out << "length: ";
    rosidl_generator_traits::value_to_yaml(msg.length, out);
    out << ", ";
  }

  // member: width
  {
    out << "width: ";
    rosidl_generator_traits::value_to_yaml(msg.width, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const VDInfo & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: x
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "x: ";
    rosidl_generator_traits::value_to_yaml(msg.x, out);
    out << "\n";
  }

  // member: y
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "y: ";
    rosidl_generator_traits::value_to_yaml(msg.y, out);
    out << "\n";
  }

  // member: yaw
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "yaw: ";
    rosidl_generator_traits::value_to_yaml(msg.yaw, out);
    out << "\n";
  }

  // member: length
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "length: ";
    rosidl_generator_traits::value_to_yaml(msg.length, out);
    out << "\n";
  }

  // member: width
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "width: ";
    rosidl_generator_traits::value_to_yaml(msg.width, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const VDInfo & msg, bool use_flow_style = false)
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
  const vd_msgs::msg::VDInfo & msg,
  std::ostream & out, size_t indentation = 0)
{
  vd_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use vd_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const vd_msgs::msg::VDInfo & msg)
{
  return vd_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<vd_msgs::msg::VDInfo>()
{
  return "vd_msgs::msg::VDInfo";
}

template<>
inline const char * name<vd_msgs::msg::VDInfo>()
{
  return "vd_msgs/msg/VDInfo";
}

template<>
struct has_fixed_size<vd_msgs::msg::VDInfo>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<vd_msgs::msg::VDInfo>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<vd_msgs::msg::VDInfo>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // VD_MSGS__MSG__DETAIL__VD_INFO__TRAITS_HPP_
