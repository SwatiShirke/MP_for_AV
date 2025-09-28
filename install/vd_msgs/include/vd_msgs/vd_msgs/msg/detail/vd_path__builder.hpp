// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from vd_msgs:msg/VDPath.idl
// generated code does not contain a copyright notice

#ifndef VD_MSGS__MSG__DETAIL__VD_PATH__BUILDER_HPP_
#define VD_MSGS__MSG__DETAIL__VD_PATH__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "vd_msgs/msg/detail/vd_path__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace vd_msgs
{

namespace msg
{

namespace builder
{

class Init_VDPath_y_val
{
public:
  explicit Init_VDPath_y_val(::vd_msgs::msg::VDPath & msg)
  : msg_(msg)
  {}
  ::vd_msgs::msg::VDPath y_val(::vd_msgs::msg::VDPath::_y_val_type arg)
  {
    msg_.y_val = std::move(arg);
    return std::move(msg_);
  }

private:
  ::vd_msgs::msg::VDPath msg_;
};

class Init_VDPath_x_val
{
public:
  Init_VDPath_x_val()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_VDPath_y_val x_val(::vd_msgs::msg::VDPath::_x_val_type arg)
  {
    msg_.x_val = std::move(arg);
    return Init_VDPath_y_val(msg_);
  }

private:
  ::vd_msgs::msg::VDPath msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::vd_msgs::msg::VDPath>()
{
  return vd_msgs::msg::builder::Init_VDPath_x_val();
}

}  // namespace vd_msgs

#endif  // VD_MSGS__MSG__DETAIL__VD_PATH__BUILDER_HPP_
