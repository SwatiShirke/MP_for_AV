// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from vd_msgs:msg/VDControlCMD.idl
// generated code does not contain a copyright notice

#ifndef VD_MSGS__MSG__DETAIL__VD_CONTROL_CMD__BUILDER_HPP_
#define VD_MSGS__MSG__DETAIL__VD_CONTROL_CMD__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "vd_msgs/msg/detail/vd_control_cmd__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace vd_msgs
{

namespace msg
{

namespace builder
{

class Init_VDControlCMD_steering_angle
{
public:
  explicit Init_VDControlCMD_steering_angle(::vd_msgs::msg::VDControlCMD & msg)
  : msg_(msg)
  {}
  ::vd_msgs::msg::VDControlCMD steering_angle(::vd_msgs::msg::VDControlCMD::_steering_angle_type arg)
  {
    msg_.steering_angle = std::move(arg);
    return std::move(msg_);
  }

private:
  ::vd_msgs::msg::VDControlCMD msg_;
};

class Init_VDControlCMD_velocity
{
public:
  Init_VDControlCMD_velocity()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_VDControlCMD_steering_angle velocity(::vd_msgs::msg::VDControlCMD::_velocity_type arg)
  {
    msg_.velocity = std::move(arg);
    return Init_VDControlCMD_steering_angle(msg_);
  }

private:
  ::vd_msgs::msg::VDControlCMD msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::vd_msgs::msg::VDControlCMD>()
{
  return vd_msgs::msg::builder::Init_VDControlCMD_velocity();
}

}  // namespace vd_msgs

#endif  // VD_MSGS__MSG__DETAIL__VD_CONTROL_CMD__BUILDER_HPP_
