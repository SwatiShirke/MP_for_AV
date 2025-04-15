// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from vd_msgs:msg/VDList.idl
// generated code does not contain a copyright notice

#ifndef VD_MSGS__MSG__DETAIL__VD_LIST__TRAITS_HPP_
#define VD_MSGS__MSG__DETAIL__VD_LIST__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "vd_msgs/msg/detail/vd_list__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'vdlist'
#include "vd_msgs/msg/detail/vd_info__traits.hpp"

namespace vd_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const VDList & msg,
  std::ostream & out)
{
  out << "{";
  // member: vdlist
  {
    if (msg.vdlist.size() == 0) {
      out << "vdlist: []";
    } else {
      out << "vdlist: [";
      size_t pending_items = msg.vdlist.size();
      for (auto item : msg.vdlist) {
        to_flow_style_yaml(item, out);
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
  const VDList & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: vdlist
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.vdlist.size() == 0) {
      out << "vdlist: []\n";
    } else {
      out << "vdlist:\n";
      for (auto item : msg.vdlist) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const VDList & msg, bool use_flow_style = false)
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
  const vd_msgs::msg::VDList & msg,
  std::ostream & out, size_t indentation = 0)
{
  vd_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use vd_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const vd_msgs::msg::VDList & msg)
{
  return vd_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<vd_msgs::msg::VDList>()
{
  return "vd_msgs::msg::VDList";
}

template<>
inline const char * name<vd_msgs::msg::VDList>()
{
  return "vd_msgs/msg/VDList";
}

template<>
struct has_fixed_size<vd_msgs::msg::VDList>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<vd_msgs::msg::VDList>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<vd_msgs::msg::VDList>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // VD_MSGS__MSG__DETAIL__VD_LIST__TRAITS_HPP_
