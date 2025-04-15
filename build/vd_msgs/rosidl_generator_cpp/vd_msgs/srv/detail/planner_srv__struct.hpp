// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from vd_msgs:srv/PlannerSrv.idl
// generated code does not contain a copyright notice

#ifndef VD_MSGS__SRV__DETAIL__PLANNER_SRV__STRUCT_HPP_
#define VD_MSGS__SRV__DETAIL__PLANNER_SRV__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__vd_msgs__srv__PlannerSrv_Request __attribute__((deprecated))
#else
# define DEPRECATED__vd_msgs__srv__PlannerSrv_Request __declspec(deprecated)
#endif

namespace vd_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct PlannerSrv_Request_
{
  using Type = PlannerSrv_Request_<ContainerAllocator>;

  explicit PlannerSrv_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->x = 0.0f;
      this->y = 0.0f;
    }
  }

  explicit PlannerSrv_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->x = 0.0f;
      this->y = 0.0f;
    }
  }

  // field types and members
  using _x_type =
    float;
  _x_type x;
  using _y_type =
    float;
  _y_type y;

  // setters for named parameter idiom
  Type & set__x(
    const float & _arg)
  {
    this->x = _arg;
    return *this;
  }
  Type & set__y(
    const float & _arg)
  {
    this->y = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    vd_msgs::srv::PlannerSrv_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const vd_msgs::srv::PlannerSrv_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<vd_msgs::srv::PlannerSrv_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<vd_msgs::srv::PlannerSrv_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      vd_msgs::srv::PlannerSrv_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<vd_msgs::srv::PlannerSrv_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      vd_msgs::srv::PlannerSrv_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<vd_msgs::srv::PlannerSrv_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<vd_msgs::srv::PlannerSrv_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<vd_msgs::srv::PlannerSrv_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__vd_msgs__srv__PlannerSrv_Request
    std::shared_ptr<vd_msgs::srv::PlannerSrv_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__vd_msgs__srv__PlannerSrv_Request
    std::shared_ptr<vd_msgs::srv::PlannerSrv_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PlannerSrv_Request_ & other) const
  {
    if (this->x != other.x) {
      return false;
    }
    if (this->y != other.y) {
      return false;
    }
    return true;
  }
  bool operator!=(const PlannerSrv_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PlannerSrv_Request_

// alias to use template instance with default allocator
using PlannerSrv_Request =
  vd_msgs::srv::PlannerSrv_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace vd_msgs


#ifndef _WIN32
# define DEPRECATED__vd_msgs__srv__PlannerSrv_Response __attribute__((deprecated))
#else
# define DEPRECATED__vd_msgs__srv__PlannerSrv_Response __declspec(deprecated)
#endif

namespace vd_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct PlannerSrv_Response_
{
  using Type = PlannerSrv_Response_<ContainerAllocator>;

  explicit PlannerSrv_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->message = "";
    }
  }

  explicit PlannerSrv_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->message = "";
    }
  }

  // field types and members
  using _message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _message_type message;

  // setters for named parameter idiom
  Type & set__message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->message = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    vd_msgs::srv::PlannerSrv_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const vd_msgs::srv::PlannerSrv_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<vd_msgs::srv::PlannerSrv_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<vd_msgs::srv::PlannerSrv_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      vd_msgs::srv::PlannerSrv_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<vd_msgs::srv::PlannerSrv_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      vd_msgs::srv::PlannerSrv_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<vd_msgs::srv::PlannerSrv_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<vd_msgs::srv::PlannerSrv_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<vd_msgs::srv::PlannerSrv_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__vd_msgs__srv__PlannerSrv_Response
    std::shared_ptr<vd_msgs::srv::PlannerSrv_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__vd_msgs__srv__PlannerSrv_Response
    std::shared_ptr<vd_msgs::srv::PlannerSrv_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PlannerSrv_Response_ & other) const
  {
    if (this->message != other.message) {
      return false;
    }
    return true;
  }
  bool operator!=(const PlannerSrv_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PlannerSrv_Response_

// alias to use template instance with default allocator
using PlannerSrv_Response =
  vd_msgs::srv::PlannerSrv_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace vd_msgs

namespace vd_msgs
{

namespace srv
{

struct PlannerSrv
{
  using Request = vd_msgs::srv::PlannerSrv_Request;
  using Response = vd_msgs::srv::PlannerSrv_Response;
};

}  // namespace srv

}  // namespace vd_msgs

#endif  // VD_MSGS__SRV__DETAIL__PLANNER_SRV__STRUCT_HPP_
