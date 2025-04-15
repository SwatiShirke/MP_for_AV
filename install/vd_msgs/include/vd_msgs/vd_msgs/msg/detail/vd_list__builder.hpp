// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from vd_msgs:msg/VDList.idl
// generated code does not contain a copyright notice

#ifndef VD_MSGS__MSG__DETAIL__VD_LIST__BUILDER_HPP_
#define VD_MSGS__MSG__DETAIL__VD_LIST__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "vd_msgs/msg/detail/vd_list__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace vd_msgs
{

namespace msg
{

namespace builder
{

class Init_VDList_vdlist
{
public:
  Init_VDList_vdlist()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::vd_msgs::msg::VDList vdlist(::vd_msgs::msg::VDList::_vdlist_type arg)
  {
    msg_.vdlist = std::move(arg);
    return std::move(msg_);
  }

private:
  ::vd_msgs::msg::VDList msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::vd_msgs::msg::VDList>()
{
  return vd_msgs::msg::builder::Init_VDList_vdlist();
}

}  // namespace vd_msgs

#endif  // VD_MSGS__MSG__DETAIL__VD_LIST__BUILDER_HPP_
