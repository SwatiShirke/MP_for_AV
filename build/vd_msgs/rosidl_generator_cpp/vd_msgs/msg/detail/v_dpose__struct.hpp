// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from vd_msgs:msg/VDpose.idl
// generated code does not contain a copyright notice

#ifndef VD_MSGS__MSG__DETAIL__V_DPOSE__STRUCT_HPP_
#define VD_MSGS__MSG__DETAIL__V_DPOSE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__vd_msgs__msg__VDpose __attribute__((deprecated))
#else
# define DEPRECATED__vd_msgs__msg__VDpose __declspec(deprecated)
#endif

namespace vd_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct VDpose_
{
  using Type = VDpose_<ContainerAllocator>;

  explicit VDpose_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->s = 0.0;
      this->x = 0.0;
      this->y = 0.0;
      this->psi = 0.0;
      this->vf = 0.0;
    }
  }

  explicit VDpose_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->s = 0.0;
      this->x = 0.0;
      this->y = 0.0;
      this->psi = 0.0;
      this->vf = 0.0;
    }
  }

  // field types and members
  using _s_type =
    double;
  _s_type s;
  using _x_type =
    double;
  _x_type x;
  using _y_type =
    double;
  _y_type y;
  using _psi_type =
    double;
  _psi_type psi;
  using _vf_type =
    double;
  _vf_type vf;

  // setters for named parameter idiom
  Type & set__s(
    const double & _arg)
  {
    this->s = _arg;
    return *this;
  }
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
  Type & set__psi(
    const double & _arg)
  {
    this->psi = _arg;
    return *this;
  }
  Type & set__vf(
    const double & _arg)
  {
    this->vf = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    vd_msgs::msg::VDpose_<ContainerAllocator> *;
  using ConstRawPtr =
    const vd_msgs::msg::VDpose_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<vd_msgs::msg::VDpose_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<vd_msgs::msg::VDpose_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      vd_msgs::msg::VDpose_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<vd_msgs::msg::VDpose_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      vd_msgs::msg::VDpose_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<vd_msgs::msg::VDpose_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<vd_msgs::msg::VDpose_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<vd_msgs::msg::VDpose_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__vd_msgs__msg__VDpose
    std::shared_ptr<vd_msgs::msg::VDpose_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__vd_msgs__msg__VDpose
    std::shared_ptr<vd_msgs::msg::VDpose_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const VDpose_ & other) const
  {
    if (this->s != other.s) {
      return false;
    }
    if (this->x != other.x) {
      return false;
    }
    if (this->y != other.y) {
      return false;
    }
    if (this->psi != other.psi) {
      return false;
    }
    if (this->vf != other.vf) {
      return false;
    }
    return true;
  }
  bool operator!=(const VDpose_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct VDpose_

// alias to use template instance with default allocator
using VDpose =
  vd_msgs::msg::VDpose_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace vd_msgs

#endif  // VD_MSGS__MSG__DETAIL__V_DPOSE__STRUCT_HPP_
