// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from vd_msgs:msg/VDInfo.idl
// generated code does not contain a copyright notice

#ifndef VD_MSGS__MSG__DETAIL__VD_INFO__BUILDER_HPP_
#define VD_MSGS__MSG__DETAIL__VD_INFO__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "vd_msgs/msg/detail/vd_info__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace vd_msgs
{

namespace msg
{

namespace builder
{

class Init_VDInfo_width
{
public:
  explicit Init_VDInfo_width(::vd_msgs::msg::VDInfo & msg)
  : msg_(msg)
  {}
  ::vd_msgs::msg::VDInfo width(::vd_msgs::msg::VDInfo::_width_type arg)
  {
    msg_.width = std::move(arg);
    return std::move(msg_);
  }

private:
  ::vd_msgs::msg::VDInfo msg_;
};

class Init_VDInfo_length
{
public:
  explicit Init_VDInfo_length(::vd_msgs::msg::VDInfo & msg)
  : msg_(msg)
  {}
  Init_VDInfo_width length(::vd_msgs::msg::VDInfo::_length_type arg)
  {
    msg_.length = std::move(arg);
    return Init_VDInfo_width(msg_);
  }

private:
  ::vd_msgs::msg::VDInfo msg_;
};

class Init_VDInfo_yaw
{
public:
  explicit Init_VDInfo_yaw(::vd_msgs::msg::VDInfo & msg)
  : msg_(msg)
  {}
  Init_VDInfo_length yaw(::vd_msgs::msg::VDInfo::_yaw_type arg)
  {
    msg_.yaw = std::move(arg);
    return Init_VDInfo_length(msg_);
  }

private:
  ::vd_msgs::msg::VDInfo msg_;
};

class Init_VDInfo_y
{
public:
  explicit Init_VDInfo_y(::vd_msgs::msg::VDInfo & msg)
  : msg_(msg)
  {}
  Init_VDInfo_yaw y(::vd_msgs::msg::VDInfo::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_VDInfo_yaw(msg_);
  }

private:
  ::vd_msgs::msg::VDInfo msg_;
};

class Init_VDInfo_x
{
public:
  Init_VDInfo_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_VDInfo_y x(::vd_msgs::msg::VDInfo::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_VDInfo_y(msg_);
  }

private:
  ::vd_msgs::msg::VDInfo msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::vd_msgs::msg::VDInfo>()
{
  return vd_msgs::msg::builder::Init_VDInfo_x();
}

}  // namespace vd_msgs

#endif  // VD_MSGS__MSG__DETAIL__VD_INFO__BUILDER_HPP_
