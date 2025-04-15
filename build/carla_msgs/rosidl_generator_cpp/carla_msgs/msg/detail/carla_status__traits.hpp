// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from carla_msgs:msg/CarlaStatus.idl
// generated code does not contain a copyright notice

#ifndef CARLA_MSGS__MSG__DETAIL__CARLA_STATUS__TRAITS_HPP_
#define CARLA_MSGS__MSG__DETAIL__CARLA_STATUS__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "carla_msgs/msg/detail/carla_status__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace carla_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const CarlaStatus & msg,
  std::ostream & out)
{
  out << "{";
  // member: frame
  {
    out << "frame: ";
    rosidl_generator_traits::value_to_yaml(msg.frame, out);
    out << ", ";
  }

  // member: fixed_delta_seconds
  {
    out << "fixed_delta_seconds: ";
    rosidl_generator_traits::value_to_yaml(msg.fixed_delta_seconds, out);
    out << ", ";
  }

  // member: synchronous_mode
  {
    out << "synchronous_mode: ";
    rosidl_generator_traits::value_to_yaml(msg.synchronous_mode, out);
    out << ", ";
  }

  // member: synchronous_mode_running
  {
    out << "synchronous_mode_running: ";
    rosidl_generator_traits::value_to_yaml(msg.synchronous_mode_running, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const CarlaStatus & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: frame
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "frame: ";
    rosidl_generator_traits::value_to_yaml(msg.frame, out);
    out << "\n";
  }

  // member: fixed_delta_seconds
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "fixed_delta_seconds: ";
    rosidl_generator_traits::value_to_yaml(msg.fixed_delta_seconds, out);
    out << "\n";
  }

  // member: synchronous_mode
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "synchronous_mode: ";
    rosidl_generator_traits::value_to_yaml(msg.synchronous_mode, out);
    out << "\n";
  }

  // member: synchronous_mode_running
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "synchronous_mode_running: ";
    rosidl_generator_traits::value_to_yaml(msg.synchronous_mode_running, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const CarlaStatus & msg, bool use_flow_style = false)
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

}  // namespace carla_msgs

namespace rosidl_generator_traits
{

[[deprecated("use carla_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const carla_msgs::msg::CarlaStatus & msg,
  std::ostream & out, size_t indentation = 0)
{
  carla_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use carla_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const carla_msgs::msg::CarlaStatus & msg)
{
  return carla_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<carla_msgs::msg::CarlaStatus>()
{
  return "carla_msgs::msg::CarlaStatus";
}

template<>
inline const char * name<carla_msgs::msg::CarlaStatus>()
{
  return "carla_msgs/msg/CarlaStatus";
}

template<>
struct has_fixed_size<carla_msgs::msg::CarlaStatus>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<carla_msgs::msg::CarlaStatus>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<carla_msgs::msg::CarlaStatus>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // CARLA_MSGS__MSG__DETAIL__CARLA_STATUS__TRAITS_HPP_
