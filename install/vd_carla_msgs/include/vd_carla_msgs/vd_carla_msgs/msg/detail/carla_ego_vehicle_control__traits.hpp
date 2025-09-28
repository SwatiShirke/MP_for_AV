// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from vd_carla_msgs:msg/CarlaEgoVehicleControl.idl
// generated code does not contain a copyright notice

#ifndef VD_CARLA_MSGS__MSG__DETAIL__CARLA_EGO_VEHICLE_CONTROL__TRAITS_HPP_
#define VD_CARLA_MSGS__MSG__DETAIL__CARLA_EGO_VEHICLE_CONTROL__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "vd_carla_msgs/msg/detail/carla_ego_vehicle_control__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace vd_carla_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const CarlaEgoVehicleControl & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: throttle
  {
    out << "throttle: ";
    rosidl_generator_traits::value_to_yaml(msg.throttle, out);
    out << ", ";
  }

  // member: steer
  {
    out << "steer: ";
    rosidl_generator_traits::value_to_yaml(msg.steer, out);
    out << ", ";
  }

  // member: brake
  {
    out << "brake: ";
    rosidl_generator_traits::value_to_yaml(msg.brake, out);
    out << ", ";
  }

  // member: hand_brake
  {
    out << "hand_brake: ";
    rosidl_generator_traits::value_to_yaml(msg.hand_brake, out);
    out << ", ";
  }

  // member: reverse
  {
    out << "reverse: ";
    rosidl_generator_traits::value_to_yaml(msg.reverse, out);
    out << ", ";
  }

  // member: gear
  {
    out << "gear: ";
    rosidl_generator_traits::value_to_yaml(msg.gear, out);
    out << ", ";
  }

  // member: manual_gear_shift
  {
    out << "manual_gear_shift: ";
    rosidl_generator_traits::value_to_yaml(msg.manual_gear_shift, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const CarlaEgoVehicleControl & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: throttle
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "throttle: ";
    rosidl_generator_traits::value_to_yaml(msg.throttle, out);
    out << "\n";
  }

  // member: steer
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "steer: ";
    rosidl_generator_traits::value_to_yaml(msg.steer, out);
    out << "\n";
  }

  // member: brake
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "brake: ";
    rosidl_generator_traits::value_to_yaml(msg.brake, out);
    out << "\n";
  }

  // member: hand_brake
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "hand_brake: ";
    rosidl_generator_traits::value_to_yaml(msg.hand_brake, out);
    out << "\n";
  }

  // member: reverse
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "reverse: ";
    rosidl_generator_traits::value_to_yaml(msg.reverse, out);
    out << "\n";
  }

  // member: gear
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "gear: ";
    rosidl_generator_traits::value_to_yaml(msg.gear, out);
    out << "\n";
  }

  // member: manual_gear_shift
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "manual_gear_shift: ";
    rosidl_generator_traits::value_to_yaml(msg.manual_gear_shift, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const CarlaEgoVehicleControl & msg, bool use_flow_style = false)
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

}  // namespace vd_carla_msgs

namespace rosidl_generator_traits
{

[[deprecated("use vd_carla_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const vd_carla_msgs::msg::CarlaEgoVehicleControl & msg,
  std::ostream & out, size_t indentation = 0)
{
  vd_carla_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use vd_carla_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const vd_carla_msgs::msg::CarlaEgoVehicleControl & msg)
{
  return vd_carla_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<vd_carla_msgs::msg::CarlaEgoVehicleControl>()
{
  return "vd_carla_msgs::msg::CarlaEgoVehicleControl";
}

template<>
inline const char * name<vd_carla_msgs::msg::CarlaEgoVehicleControl>()
{
  return "vd_carla_msgs/msg/CarlaEgoVehicleControl";
}

template<>
struct has_fixed_size<vd_carla_msgs::msg::CarlaEgoVehicleControl>
  : std::integral_constant<bool, has_fixed_size<std_msgs::msg::Header>::value> {};

template<>
struct has_bounded_size<vd_carla_msgs::msg::CarlaEgoVehicleControl>
  : std::integral_constant<bool, has_bounded_size<std_msgs::msg::Header>::value> {};

template<>
struct is_message<vd_carla_msgs::msg::CarlaEgoVehicleControl>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // VD_CARLA_MSGS__MSG__DETAIL__CARLA_EGO_VEHICLE_CONTROL__TRAITS_HPP_
