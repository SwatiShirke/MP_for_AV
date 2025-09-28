// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from vd_msgs:msg/VDstate.idl
// generated code does not contain a copyright notice

#ifndef VD_MSGS__MSG__DETAIL__V_DSTATE__TRAITS_HPP_
#define VD_MSGS__MSG__DETAIL__V_DSTATE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "vd_msgs/msg/detail/v_dstate__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace vd_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const VDstate & msg,
  std::ostream & out)
{
  out << "{";
  // member: vx
  {
    out << "vx: ";
    rosidl_generator_traits::value_to_yaml(msg.vx, out);
    out << ", ";
  }

  // member: vy
  {
    out << "vy: ";
    rosidl_generator_traits::value_to_yaml(msg.vy, out);
    out << ", ";
  }

  // member: r
  {
    out << "r: ";
    rosidl_generator_traits::value_to_yaml(msg.r, out);
    out << ", ";
  }

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

  // member: psi
  {
    out << "psi: ";
    rosidl_generator_traits::value_to_yaml(msg.psi, out);
    out << ", ";
  }

  // member: w_fl
  {
    out << "w_fl: ";
    rosidl_generator_traits::value_to_yaml(msg.w_fl, out);
    out << ", ";
  }

  // member: w_fr
  {
    out << "w_fr: ";
    rosidl_generator_traits::value_to_yaml(msg.w_fr, out);
    out << ", ";
  }

  // member: w_rl
  {
    out << "w_rl: ";
    rosidl_generator_traits::value_to_yaml(msg.w_rl, out);
    out << ", ";
  }

  // member: w_rr
  {
    out << "w_rr: ";
    rosidl_generator_traits::value_to_yaml(msg.w_rr, out);
    out << ", ";
  }

  // member: s
  {
    out << "s: ";
    rosidl_generator_traits::value_to_yaml(msg.s, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const VDstate & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: vx
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "vx: ";
    rosidl_generator_traits::value_to_yaml(msg.vx, out);
    out << "\n";
  }

  // member: vy
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "vy: ";
    rosidl_generator_traits::value_to_yaml(msg.vy, out);
    out << "\n";
  }

  // member: r
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "r: ";
    rosidl_generator_traits::value_to_yaml(msg.r, out);
    out << "\n";
  }

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

  // member: psi
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "psi: ";
    rosidl_generator_traits::value_to_yaml(msg.psi, out);
    out << "\n";
  }

  // member: w_fl
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "w_fl: ";
    rosidl_generator_traits::value_to_yaml(msg.w_fl, out);
    out << "\n";
  }

  // member: w_fr
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "w_fr: ";
    rosidl_generator_traits::value_to_yaml(msg.w_fr, out);
    out << "\n";
  }

  // member: w_rl
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "w_rl: ";
    rosidl_generator_traits::value_to_yaml(msg.w_rl, out);
    out << "\n";
  }

  // member: w_rr
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "w_rr: ";
    rosidl_generator_traits::value_to_yaml(msg.w_rr, out);
    out << "\n";
  }

  // member: s
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "s: ";
    rosidl_generator_traits::value_to_yaml(msg.s, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const VDstate & msg, bool use_flow_style = false)
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
  const vd_msgs::msg::VDstate & msg,
  std::ostream & out, size_t indentation = 0)
{
  vd_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use vd_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const vd_msgs::msg::VDstate & msg)
{
  return vd_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<vd_msgs::msg::VDstate>()
{
  return "vd_msgs::msg::VDstate";
}

template<>
inline const char * name<vd_msgs::msg::VDstate>()
{
  return "vd_msgs/msg/VDstate";
}

template<>
struct has_fixed_size<vd_msgs::msg::VDstate>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<vd_msgs::msg::VDstate>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<vd_msgs::msg::VDstate>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // VD_MSGS__MSG__DETAIL__V_DSTATE__TRAITS_HPP_
