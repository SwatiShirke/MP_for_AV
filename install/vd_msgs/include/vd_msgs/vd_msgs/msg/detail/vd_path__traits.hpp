// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from vd_msgs:msg/VDPath.idl
// generated code does not contain a copyright notice

#ifndef VD_MSGS__MSG__DETAIL__VD_PATH__TRAITS_HPP_
#define VD_MSGS__MSG__DETAIL__VD_PATH__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "vd_msgs/msg/detail/vd_path__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace vd_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const VDPath & msg,
  std::ostream & out)
{
  out << "{";
  // member: x_val
  {
    if (msg.x_val.size() == 0) {
      out << "x_val: []";
    } else {
      out << "x_val: [";
      size_t pending_items = msg.x_val.size();
      for (auto item : msg.x_val) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: y_val
  {
    if (msg.y_val.size() == 0) {
      out << "y_val: []";
    } else {
      out << "y_val: [";
      size_t pending_items = msg.y_val.size();
      for (auto item : msg.y_val) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const VDPath & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: x_val
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.x_val.size() == 0) {
      out << "x_val: []\n";
    } else {
      out << "x_val:\n";
      for (auto item : msg.x_val) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: y_val
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.y_val.size() == 0) {
      out << "y_val: []\n";
    } else {
      out << "y_val:\n";
      for (auto item : msg.y_val) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const VDPath & msg, bool use_flow_style = false)
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
  const vd_msgs::msg::VDPath & msg,
  std::ostream & out, size_t indentation = 0)
{
  vd_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use vd_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const vd_msgs::msg::VDPath & msg)
{
  return vd_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<vd_msgs::msg::VDPath>()
{
  return "vd_msgs::msg::VDPath";
}

template<>
inline const char * name<vd_msgs::msg::VDPath>()
{
  return "vd_msgs/msg/VDPath";
}

template<>
struct has_fixed_size<vd_msgs::msg::VDPath>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<vd_msgs::msg::VDPath>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<vd_msgs::msg::VDPath>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // VD_MSGS__MSG__DETAIL__VD_PATH__TRAITS_HPP_
