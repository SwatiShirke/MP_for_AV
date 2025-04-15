// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from vd_msgs:msg/VDInfo.idl
// generated code does not contain a copyright notice

#ifndef VD_MSGS__MSG__DETAIL__VD_INFO__STRUCT_HPP_
#define VD_MSGS__MSG__DETAIL__VD_INFO__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__vd_msgs__msg__VDInfo __attribute__((deprecated))
#else
# define DEPRECATED__vd_msgs__msg__VDInfo __declspec(deprecated)
#endif

namespace vd_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct VDInfo_
{
  using Type = VDInfo_<ContainerAllocator>;

  explicit VDInfo_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->x = 0.0;
      this->y = 0.0;
      this->yaw = 0.0;
      this->length = 0.0;
      this->width = 0.0;
    }
  }

  explicit VDInfo_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->x = 0.0;
      this->y = 0.0;
      this->yaw = 0.0;
      this->length = 0.0;
      this->width = 0.0;
    }
  }

  // field types and members
  using _x_type =
    double;
  _x_type x;
  using _y_type =
    double;
  _y_type y;
  using _yaw_type =
    double;
  _yaw_type yaw;
  using _length_type =
    double;
  _length_type length;
  using _width_type =
    double;
  _width_type width;

  // setters for named parameter idiom
  Type & set__x(
    const double & _arg)
  {
    this->x = _arg;
    return *this;
  }
  Type & set__y(
    const double & _arg)
  {
    this->y = _arg;
    return *this;
  }
  Type & set__yaw(
    const double & _arg)
  {
    this->yaw = _arg;
    return *this;
  }
  Type & set__length(
    const double & _arg)
  {
    this->length = _arg;
    return *this;
  }
  Type & set__width(
    const double & _arg)
  {
    this->width = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    vd_msgs::msg::VDInfo_<ContainerAllocator> *;
  using ConstRawPtr =
    const vd_msgs::msg::VDInfo_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<vd_msgs::msg::VDInfo_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<vd_msgs::msg::VDInfo_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      vd_msgs::msg::VDInfo_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<vd_msgs::msg::VDInfo_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      vd_msgs::msg::VDInfo_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<vd_msgs::msg::VDInfo_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<vd_msgs::msg::VDInfo_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<vd_msgs::msg::VDInfo_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__vd_msgs__msg__VDInfo
    std::shared_ptr<vd_msgs::msg::VDInfo_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__vd_msgs__msg__VDInfo
    std::shared_ptr<vd_msgs::msg::VDInfo_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const VDInfo_ & other) const
  {
    if (this->x != other.x) {
      return false;
    }
    if (this->y != other.y) {
      return false;
    }
    if (this->yaw != other.yaw) {
      return false;
    }
    if (this->length != other.length) {
      return false;
    }
    if (this->width != other.width) {
      return false;
    }
    return true;
  }
  bool operator!=(const VDInfo_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct VDInfo_

// alias to use template instance with default allocator
using VDInfo =
  vd_msgs::msg::VDInfo_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace vd_msgs

#endif  // VD_MSGS__MSG__DETAIL__VD_INFO__STRUCT_HPP_
