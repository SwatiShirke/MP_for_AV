// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from vd_msgs:srv/PlannerSrv.idl
// generated code does not contain a copyright notice

#ifndef VD_MSGS__SRV__DETAIL__PLANNER_SRV__BUILDER_HPP_
#define VD_MSGS__SRV__DETAIL__PLANNER_SRV__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "vd_msgs/srv/detail/planner_srv__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace vd_msgs
{

namespace srv
{

namespace builder
{

class Init_PlannerSrv_Request_y
{
public:
  explicit Init_PlannerSrv_Request_y(::vd_msgs::srv::PlannerSrv_Request & msg)
  : msg_(msg)
  {}
  ::vd_msgs::srv::PlannerSrv_Request y(::vd_msgs::srv::PlannerSrv_Request::_y_type arg)
  {
    msg_.y = std::move(arg);
    return std::move(msg_);
  }

private:
  ::vd_msgs::srv::PlannerSrv_Request msg_;
};

class Init_PlannerSrv_Request_x
{
public:
  Init_PlannerSrv_Request_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PlannerSrv_Request_y x(::vd_msgs::srv::PlannerSrv_Request::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_PlannerSrv_Request_y(msg_);
  }

private:
  ::vd_msgs::srv::PlannerSrv_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::vd_msgs::srv::PlannerSrv_Request>()
{
  return vd_msgs::srv::builder::Init_PlannerSrv_Request_x();
}

}  // namespace vd_msgs


namespace vd_msgs
{

namespace srv
{

namespace builder
{

class Init_PlannerSrv_Response_message
{
public:
  Init_PlannerSrv_Response_message()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::vd_msgs::srv::PlannerSrv_Response message(::vd_msgs::srv::PlannerSrv_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::vd_msgs::srv::PlannerSrv_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::vd_msgs::srv::PlannerSrv_Response>()
{
  return vd_msgs::srv::builder::Init_PlannerSrv_Response_message();
}

}  // namespace vd_msgs

#endif  // VD_MSGS__SRV__DETAIL__PLANNER_SRV__BUILDER_HPP_
