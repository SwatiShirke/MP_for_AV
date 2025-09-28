// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from vd_msgs:msg/VDstate.idl
// generated code does not contain a copyright notice

#ifndef VD_MSGS__MSG__DETAIL__V_DSTATE__BUILDER_HPP_
#define VD_MSGS__MSG__DETAIL__V_DSTATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "vd_msgs/msg/detail/v_dstate__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace vd_msgs
{

namespace msg
{

namespace builder
{

class Init_VDstate_s
{
public:
  explicit Init_VDstate_s(::vd_msgs::msg::VDstate & msg)
  : msg_(msg)
  {}
  ::vd_msgs::msg::VDstate s(::vd_msgs::msg::VDstate::_s_type arg)
  {
    msg_.s = std::move(arg);
    return std::move(msg_);
  }

private:
  ::vd_msgs::msg::VDstate msg_;
};

class Init_VDstate_w_rr
{
public:
  explicit Init_VDstate_w_rr(::vd_msgs::msg::VDstate & msg)
  : msg_(msg)
  {}
  Init_VDstate_s w_rr(::vd_msgs::msg::VDstate::_w_rr_type arg)
  {
    msg_.w_rr = std::move(arg);
    return Init_VDstate_s(msg_);
  }

private:
  ::vd_msgs::msg::VDstate msg_;
};

class Init_VDstate_w_rl
{
public:
  explicit Init_VDstate_w_rl(::vd_msgs::msg::VDstate & msg)
  : msg_(msg)
  {}
  Init_VDstate_w_rr w_rl(::vd_msgs::msg::VDstate::_w_rl_type arg)
  {
    msg_.w_rl = std::move(arg);
    return Init_VDstate_w_rr(msg_);
  }

private:
  ::vd_msgs::msg::VDstate msg_;
};

class Init_VDstate_w_fr
{
public:
  explicit Init_VDstate_w_fr(::vd_msgs::msg::VDstate & msg)
  : msg_(msg)
  {}
  Init_VDstate_w_rl w_fr(::vd_msgs::msg::VDstate::_w_fr_type arg)
  {
    msg_.w_fr = std::move(arg);
    return Init_VDstate_w_rl(msg_);
  }

private:
  ::vd_msgs::msg::VDstate msg_;
};

class Init_VDstate_w_fl
{
public:
  explicit Init_VDstate_w_fl(::vd_msgs::msg::VDstate & msg)
  : msg_(msg)
  {}
  Init_VDstate_w_fr w_fl(::vd_msgs::msg::VDstate::_w_fl_type arg)
  {
    msg_.w_fl = std::move(arg);
    return Init_VDstate_w_fr(msg_);
  }

private:
  ::vd_msgs::msg::VDstate msg_;
};

class Init_VDstate_psi
{
public:
  explicit Init_VDstate_psi(::vd_msgs::msg::VDstate & msg)
  : msg_(msg)
  {}
  Init_VDstate_w_fl psi(::vd_msgs::msg::VDstate::_psi_type arg)
  {
    msg_.psi = std::move(arg);
    return Init_VDstate_w_fl(msg_);
  }

private:
  ::vd_msgs::msg::VDstate msg_;
};

class Init_VDstate_y
{
public:
  explicit Init_VDstate_y(::vd_msgs::msg::VDstate & msg)
  : msg_(msg)
  {}
  Init_VDstate_psi y(::vd_msgs::msg::VDstate::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_VDstate_psi(msg_);
  }

private:
  ::vd_msgs::msg::VDstate msg_;
};

class Init_VDstate_x
{
public:
  explicit Init_VDstate_x(::vd_msgs::msg::VDstate & msg)
  : msg_(msg)
  {}
  Init_VDstate_y x(::vd_msgs::msg::VDstate::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_VDstate_y(msg_);
  }

private:
  ::vd_msgs::msg::VDstate msg_;
};

class Init_VDstate_r
{
public:
  explicit Init_VDstate_r(::vd_msgs::msg::VDstate & msg)
  : msg_(msg)
  {}
  Init_VDstate_x r(::vd_msgs::msg::VDstate::_r_type arg)
  {
    msg_.r = std::move(arg);
    return Init_VDstate_x(msg_);
  }

private:
  ::vd_msgs::msg::VDstate msg_;
};

class Init_VDstate_vy
{
public:
  explicit Init_VDstate_vy(::vd_msgs::msg::VDstate & msg)
  : msg_(msg)
  {}
  Init_VDstate_r vy(::vd_msgs::msg::VDstate::_vy_type arg)
  {
    msg_.vy = std::move(arg);
    return Init_VDstate_r(msg_);
  }

private:
  ::vd_msgs::msg::VDstate msg_;
};

class Init_VDstate_vx
{
public:
  Init_VDstate_vx()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_VDstate_vy vx(::vd_msgs::msg::VDstate::_vx_type arg)
  {
    msg_.vx = std::move(arg);
    return Init_VDstate_vy(msg_);
  }

private:
  ::vd_msgs::msg::VDstate msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::vd_msgs::msg::VDstate>()
{
  return vd_msgs::msg::builder::Init_VDstate_vx();
}

}  // namespace vd_msgs

#endif  // VD_MSGS__MSG__DETAIL__V_DSTATE__BUILDER_HPP_
