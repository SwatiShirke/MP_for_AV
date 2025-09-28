// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from vd_msgs:msg/VDpose.idl
// generated code does not contain a copyright notice

#ifndef VD_MSGS__MSG__DETAIL__V_DPOSE__BUILDER_HPP_
#define VD_MSGS__MSG__DETAIL__V_DPOSE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "vd_msgs/msg/detail/v_dpose__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace vd_msgs
{

namespace msg
{

namespace builder
{

class Init_VDpose_width
{
public:
  explicit Init_VDpose_width(::vd_msgs::msg::VDpose & msg)
  : msg_(msg)
  {}
  ::vd_msgs::msg::VDpose width(::vd_msgs::msg::VDpose::_width_type arg)
  {
    msg_.width = std::move(arg);
    return std::move(msg_);
  }

private:
  ::vd_msgs::msg::VDpose msg_;
};

class Init_VDpose_length
{
public:
  explicit Init_VDpose_length(::vd_msgs::msg::VDpose & msg)
  : msg_(msg)
  {}
  Init_VDpose_width length(::vd_msgs::msg::VDpose::_length_type arg)
  {
    msg_.length = std::move(arg);
    return Init_VDpose_width(msg_);
  }

private:
  ::vd_msgs::msg::VDpose msg_;
};

class Init_VDpose_steering_angle
{
public:
  explicit Init_VDpose_steering_angle(::vd_msgs::msg::VDpose & msg)
  : msg_(msg)
  {}
  Init_VDpose_length steering_angle(::vd_msgs::msg::VDpose::_steering_angle_type arg)
  {
    msg_.steering_angle = std::move(arg);
    return Init_VDpose_length(msg_);
  }

private:
  ::vd_msgs::msg::VDpose msg_;
};

class Init_VDpose_acceleration
{
public:
  explicit Init_VDpose_acceleration(::vd_msgs::msg::VDpose & msg)
  : msg_(msg)
  {}
  Init_VDpose_steering_angle acceleration(::vd_msgs::msg::VDpose::_acceleration_type arg)
  {
    msg_.acceleration = std::move(arg);
    return Init_VDpose_steering_angle(msg_);
  }

private:
  ::vd_msgs::msg::VDpose msg_;
};

class Init_VDpose_total_distance
{
public:
  explicit Init_VDpose_total_distance(::vd_msgs::msg::VDpose & msg)
  : msg_(msg)
  {}
  Init_VDpose_acceleration total_distance(::vd_msgs::msg::VDpose::_total_distance_type arg)
  {
    msg_.total_distance = std::move(arg);
    return Init_VDpose_acceleration(msg_);
  }

private:
  ::vd_msgs::msg::VDpose msg_;
};

class Init_VDpose_yaw_lane_center
{
public:
  explicit Init_VDpose_yaw_lane_center(::vd_msgs::msg::VDpose & msg)
  : msg_(msg)
  {}
  Init_VDpose_total_distance yaw_lane_center(::vd_msgs::msg::VDpose::_yaw_lane_center_type arg)
  {
    msg_.yaw_lane_center = std::move(arg);
    return Init_VDpose_total_distance(msg_);
  }

private:
  ::vd_msgs::msg::VDpose msg_;
};

class Init_VDpose_y_lane_center
{
public:
  explicit Init_VDpose_y_lane_center(::vd_msgs::msg::VDpose & msg)
  : msg_(msg)
  {}
  Init_VDpose_yaw_lane_center y_lane_center(::vd_msgs::msg::VDpose::_y_lane_center_type arg)
  {
    msg_.y_lane_center = std::move(arg);
    return Init_VDpose_yaw_lane_center(msg_);
  }

private:
  ::vd_msgs::msg::VDpose msg_;
};

class Init_VDpose_x_lane_center
{
public:
  explicit Init_VDpose_x_lane_center(::vd_msgs::msg::VDpose & msg)
  : msg_(msg)
  {}
  Init_VDpose_y_lane_center x_lane_center(::vd_msgs::msg::VDpose::_x_lane_center_type arg)
  {
    msg_.x_lane_center = std::move(arg);
    return Init_VDpose_y_lane_center(msg_);
  }

private:
  ::vd_msgs::msg::VDpose msg_;
};

class Init_VDpose_distance
{
public:
  explicit Init_VDpose_distance(::vd_msgs::msg::VDpose & msg)
  : msg_(msg)
  {}
  Init_VDpose_x_lane_center distance(::vd_msgs::msg::VDpose::_distance_type arg)
  {
    msg_.distance = std::move(arg);
    return Init_VDpose_x_lane_center(msg_);
  }

private:
  ::vd_msgs::msg::VDpose msg_;
};

class Init_VDpose_velocity
{
public:
  explicit Init_VDpose_velocity(::vd_msgs::msg::VDpose & msg)
  : msg_(msg)
  {}
  Init_VDpose_distance velocity(::vd_msgs::msg::VDpose::_velocity_type arg)
  {
    msg_.velocity = std::move(arg);
    return Init_VDpose_distance(msg_);
  }

private:
  ::vd_msgs::msg::VDpose msg_;
};

class Init_VDpose_psi
{
public:
  explicit Init_VDpose_psi(::vd_msgs::msg::VDpose & msg)
  : msg_(msg)
  {}
  Init_VDpose_velocity psi(::vd_msgs::msg::VDpose::_psi_type arg)
  {
    msg_.psi = std::move(arg);
    return Init_VDpose_velocity(msg_);
  }

private:
  ::vd_msgs::msg::VDpose msg_;
};

class Init_VDpose_y
{
public:
  explicit Init_VDpose_y(::vd_msgs::msg::VDpose & msg)
  : msg_(msg)
  {}
  Init_VDpose_psi y(::vd_msgs::msg::VDpose::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_VDpose_psi(msg_);
  }

private:
  ::vd_msgs::msg::VDpose msg_;
};

class Init_VDpose_x
{
public:
  explicit Init_VDpose_x(::vd_msgs::msg::VDpose & msg)
  : msg_(msg)
  {}
  Init_VDpose_y x(::vd_msgs::msg::VDpose::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_VDpose_y(msg_);
  }

private:
  ::vd_msgs::msg::VDpose msg_;
};

class Init_VDpose_header
{
public:
  Init_VDpose_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_VDpose_x header(::vd_msgs::msg::VDpose::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_VDpose_x(msg_);
  }

private:
  ::vd_msgs::msg::VDpose msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::vd_msgs::msg::VDpose>()
{
  return vd_msgs::msg::builder::Init_VDpose_header();
}

}  // namespace vd_msgs

#endif  // VD_MSGS__MSG__DETAIL__V_DPOSE__BUILDER_HPP_
