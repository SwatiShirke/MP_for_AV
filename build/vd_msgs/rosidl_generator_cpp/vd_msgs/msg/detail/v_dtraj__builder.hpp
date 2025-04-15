// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from vd_msgs:msg/VDtraj.idl
// generated code does not contain a copyright notice

#ifndef VD_MSGS__MSG__DETAIL__V_DTRAJ__BUILDER_HPP_
#define VD_MSGS__MSG__DETAIL__V_DTRAJ__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "vd_msgs/msg/detail/v_dtraj__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace vd_msgs
{

namespace msg
{

namespace builder
{

class Init_VDtraj_poses
{
public:
  Init_VDtraj_poses()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::vd_msgs::msg::VDtraj poses(::vd_msgs::msg::VDtraj::_poses_type arg)
  {
    msg_.poses = std::move(arg);
    return std::move(msg_);
  }

private:
  ::vd_msgs::msg::VDtraj msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::vd_msgs::msg::VDtraj>()
{
  return vd_msgs::msg::builder::Init_VDtraj_poses();
}

}  // namespace vd_msgs

#endif  // VD_MSGS__MSG__DETAIL__V_DTRAJ__BUILDER_HPP_
