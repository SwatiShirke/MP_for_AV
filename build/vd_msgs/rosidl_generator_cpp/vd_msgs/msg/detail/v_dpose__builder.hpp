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

class Init_VDpose_vf
{
public:
  explicit Init_VDpose_vf(::vd_msgs::msg::VDpose & msg)
  : msg_(msg)
  {}
  ::vd_msgs::msg::VDpose vf(::vd_msgs::msg::VDpose::_vf_type arg)
  {
    msg_.vf = std::move(arg);
    return std::move(msg_);
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
  Init_VDpose_vf psi(::vd_msgs::msg::VDpose::_psi_type arg)
  {
    msg_.psi = std::move(arg);
    return Init_VDpose_vf(msg_);
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

class Init_VDpose_s
{
public:
  Init_VDpose_s()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_VDpose_x s(::vd_msgs::msg::VDpose::_s_type arg)
  {
    msg_.s = std::move(arg);
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
  return vd_msgs::msg::builder::Init_VDpose_s();
}

}  // namespace vd_msgs

#endif  // VD_MSGS__MSG__DETAIL__V_DPOSE__BUILDER_HPP_
