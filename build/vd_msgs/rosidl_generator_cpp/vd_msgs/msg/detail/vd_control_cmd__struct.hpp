// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from vd_msgs:msg/VDControlCMD.idl
// generated code does not contain a copyright notice

#ifndef VD_MSGS__MSG__DETAIL__VD_CONTROL_CMD__STRUCT_HPP_
#define VD_MSGS__MSG__DETAIL__VD_CONTROL_CMD__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__vd_msgs__msg__VDControlCMD __attribute__((deprecated))
#else
# define DEPRECATED__vd_msgs__msg__VDControlCMD __declspec(deprecated)
#endif

namespace vd_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct VDControlCMD_
{
  using Type = VDControlCMD_<ContainerAllocator>;

  explicit VDControlCMD_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->velocity = 0.0;
      this->steering_angle = 0.0;
    }
  }

  explicit VDControlCMD_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->velocity = 0.0;
      this->steering_angle = 0.0;
    }
  }

  // field types and members
  using _velocity_type =
    double;
  _velocity_type velocity;
  using _steering_angle_type =
    double;
  _steering_angle_type steering_angle;

  // setters for named parameter idiom
  Type & set__velocity(
    const double & _arg)
  {
    this->velocity = _arg;
    return *this;
  }
  Type & set__steering_angle(
    const double & _arg)
  {
    this->steering_angle = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    vd_msgs::msg::VDControlCMD_<ContainerAllocator> *;
  using ConstRawPtr =
    const vd_msgs::msg::VDControlCMD_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<vd_msgs::msg::VDControlCMD_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<vd_msgs::msg::VDControlCMD_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      vd_msgs::msg::VDControlCMD_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<vd_msgs::msg::VDControlCMD_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      vd_msgs::msg::VDControlCMD_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<vd_msgs::msg::VDControlCMD_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<vd_msgs::msg::VDControlCMD_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<vd_msgs::msg::VDControlCMD_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__vd_msgs__msg__VDControlCMD
    std::shared_ptr<vd_msgs::msg::VDControlCMD_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__vd_msgs__msg__VDControlCMD
    std::shared_ptr<vd_msgs::msg::VDControlCMD_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const VDControlCMD_ & other) const
  {
    if (this->velocity != other.velocity) {
      return false;
    }
    if (this->steering_angle != other.steering_angle) {
      return false;
    }
    return true;
  }
  bool operator!=(const VDControlCMD_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct VDControlCMD_

// alias to use template instance with default allocator
using VDControlCMD =
  vd_msgs::msg::VDControlCMD_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace vd_msgs

#endif  // VD_MSGS__MSG__DETAIL__VD_CONTROL_CMD__STRUCT_HPP_
