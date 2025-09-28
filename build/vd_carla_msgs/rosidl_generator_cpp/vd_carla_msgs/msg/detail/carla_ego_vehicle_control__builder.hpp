// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from vd_carla_msgs:msg/CarlaEgoVehicleControl.idl
// generated code does not contain a copyright notice

#ifndef VD_CARLA_MSGS__MSG__DETAIL__CARLA_EGO_VEHICLE_CONTROL__BUILDER_HPP_
#define VD_CARLA_MSGS__MSG__DETAIL__CARLA_EGO_VEHICLE_CONTROL__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "vd_carla_msgs/msg/detail/carla_ego_vehicle_control__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace vd_carla_msgs
{

namespace msg
{

namespace builder
{

class Init_CarlaEgoVehicleControl_manual_gear_shift
{
public:
  explicit Init_CarlaEgoVehicleControl_manual_gear_shift(::vd_carla_msgs::msg::CarlaEgoVehicleControl & msg)
  : msg_(msg)
  {}
  ::vd_carla_msgs::msg::CarlaEgoVehicleControl manual_gear_shift(::vd_carla_msgs::msg::CarlaEgoVehicleControl::_manual_gear_shift_type arg)
  {
    msg_.manual_gear_shift = std::move(arg);
    return std::move(msg_);
  }

private:
  ::vd_carla_msgs::msg::CarlaEgoVehicleControl msg_;
};

class Init_CarlaEgoVehicleControl_gear
{
public:
  explicit Init_CarlaEgoVehicleControl_gear(::vd_carla_msgs::msg::CarlaEgoVehicleControl & msg)
  : msg_(msg)
  {}
  Init_CarlaEgoVehicleControl_manual_gear_shift gear(::vd_carla_msgs::msg::CarlaEgoVehicleControl::_gear_type arg)
  {
    msg_.gear = std::move(arg);
    return Init_CarlaEgoVehicleControl_manual_gear_shift(msg_);
  }

private:
  ::vd_carla_msgs::msg::CarlaEgoVehicleControl msg_;
};

class Init_CarlaEgoVehicleControl_reverse
{
public:
  explicit Init_CarlaEgoVehicleControl_reverse(::vd_carla_msgs::msg::CarlaEgoVehicleControl & msg)
  : msg_(msg)
  {}
  Init_CarlaEgoVehicleControl_gear reverse(::vd_carla_msgs::msg::CarlaEgoVehicleControl::_reverse_type arg)
  {
    msg_.reverse = std::move(arg);
    return Init_CarlaEgoVehicleControl_gear(msg_);
  }

private:
  ::vd_carla_msgs::msg::CarlaEgoVehicleControl msg_;
};

class Init_CarlaEgoVehicleControl_hand_brake
{
public:
  explicit Init_CarlaEgoVehicleControl_hand_brake(::vd_carla_msgs::msg::CarlaEgoVehicleControl & msg)
  : msg_(msg)
  {}
  Init_CarlaEgoVehicleControl_reverse hand_brake(::vd_carla_msgs::msg::CarlaEgoVehicleControl::_hand_brake_type arg)
  {
    msg_.hand_brake = std::move(arg);
    return Init_CarlaEgoVehicleControl_reverse(msg_);
  }

private:
  ::vd_carla_msgs::msg::CarlaEgoVehicleControl msg_;
};

class Init_CarlaEgoVehicleControl_brake
{
public:
  explicit Init_CarlaEgoVehicleControl_brake(::vd_carla_msgs::msg::CarlaEgoVehicleControl & msg)
  : msg_(msg)
  {}
  Init_CarlaEgoVehicleControl_hand_brake brake(::vd_carla_msgs::msg::CarlaEgoVehicleControl::_brake_type arg)
  {
    msg_.brake = std::move(arg);
    return Init_CarlaEgoVehicleControl_hand_brake(msg_);
  }

private:
  ::vd_carla_msgs::msg::CarlaEgoVehicleControl msg_;
};

class Init_CarlaEgoVehicleControl_steer
{
public:
  explicit Init_CarlaEgoVehicleControl_steer(::vd_carla_msgs::msg::CarlaEgoVehicleControl & msg)
  : msg_(msg)
  {}
  Init_CarlaEgoVehicleControl_brake steer(::vd_carla_msgs::msg::CarlaEgoVehicleControl::_steer_type arg)
  {
    msg_.steer = std::move(arg);
    return Init_CarlaEgoVehicleControl_brake(msg_);
  }

private:
  ::vd_carla_msgs::msg::CarlaEgoVehicleControl msg_;
};

class Init_CarlaEgoVehicleControl_throttle
{
public:
  explicit Init_CarlaEgoVehicleControl_throttle(::vd_carla_msgs::msg::CarlaEgoVehicleControl & msg)
  : msg_(msg)
  {}
  Init_CarlaEgoVehicleControl_steer throttle(::vd_carla_msgs::msg::CarlaEgoVehicleControl::_throttle_type arg)
  {
    msg_.throttle = std::move(arg);
    return Init_CarlaEgoVehicleControl_steer(msg_);
  }

private:
  ::vd_carla_msgs::msg::CarlaEgoVehicleControl msg_;
};

class Init_CarlaEgoVehicleControl_header
{
public:
  Init_CarlaEgoVehicleControl_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_CarlaEgoVehicleControl_throttle header(::vd_carla_msgs::msg::CarlaEgoVehicleControl::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_CarlaEgoVehicleControl_throttle(msg_);
  }

private:
  ::vd_carla_msgs::msg::CarlaEgoVehicleControl msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::vd_carla_msgs::msg::CarlaEgoVehicleControl>()
{
  return vd_carla_msgs::msg::builder::Init_CarlaEgoVehicleControl_header();
}

}  // namespace vd_carla_msgs

#endif  // VD_CARLA_MSGS__MSG__DETAIL__CARLA_EGO_VEHICLE_CONTROL__BUILDER_HPP_
