// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from vd_msgs:msg/VDstate.idl
// generated code does not contain a copyright notice

#ifndef VD_MSGS__MSG__DETAIL__V_DSTATE__STRUCT_HPP_
#define VD_MSGS__MSG__DETAIL__V_DSTATE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__vd_msgs__msg__VDstate __attribute__((deprecated))
#else
# define DEPRECATED__vd_msgs__msg__VDstate __declspec(deprecated)
#endif

namespace vd_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct VDstate_
{
  using Type = VDstate_<ContainerAllocator>;

  explicit VDstate_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->vx = 0.0;
      this->vy = 0.0;
      this->r = 0.0;
      this->x = 0.0;
      this->y = 0.0;
      this->psi = 0.0;
      this->w_fl = 0.0;
      this->w_fr = 0.0;
      this->w_rl = 0.0;
      this->w_rr = 0.0;
      this->s = 0.0;
    }
  }

  explicit VDstate_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->vx = 0.0;
      this->vy = 0.0;
      this->r = 0.0;
      this->x = 0.0;
      this->y = 0.0;
      this->psi = 0.0;
      this->w_fl = 0.0;
      this->w_fr = 0.0;
      this->w_rl = 0.0;
      this->w_rr = 0.0;
      this->s = 0.0;
    }
  }

  // field types and members
  using _vx_type =
    double;
  _vx_type vx;
  using _vy_type =
    double;
  _vy_type vy;
  using _r_type =
    double;
  _r_type r;
  using _x_type =
    double;
  _x_type x;
  using _y_type =
    double;
  _y_type y;
  using _psi_type =
    double;
  _psi_type psi;
  using _w_fl_type =
    double;
  _w_fl_type w_fl;
  using _w_fr_type =
    double;
  _w_fr_type w_fr;
  using _w_rl_type =
    double;
  _w_rl_type w_rl;
  using _w_rr_type =
    double;
  _w_rr_type w_rr;
  using _s_type =
    double;
  _s_type s;

  // setters for named parameter idiom
  Type & set__vx(
    const double & _arg)
  {
    this->vx = _arg;
    return *this;
  }
  Type & set__vy(
    const double & _arg)
  {
    this->vy = _arg;
    return *this;
  }
  Type & set__r(
    const double & _arg)
  {
    this->r = _arg;
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
  Type & set__w_fl(
    const double & _arg)
  {
    this->w_fl = _arg;
    return *this;
  }
  Type & set__w_fr(
    const double & _arg)
  {
    this->w_fr = _arg;
    return *this;
  }
  Type & set__w_rl(
    const double & _arg)
  {
    this->w_rl = _arg;
    return *this;
  }
  Type & set__w_rr(
    const double & _arg)
  {
    this->w_rr = _arg;
    return *this;
  }
  Type & set__s(
    const double & _arg)
  {
    this->s = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    vd_msgs::msg::VDstate_<ContainerAllocator> *;
  using ConstRawPtr =
    const vd_msgs::msg::VDstate_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<vd_msgs::msg::VDstate_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<vd_msgs::msg::VDstate_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      vd_msgs::msg::VDstate_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<vd_msgs::msg::VDstate_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      vd_msgs::msg::VDstate_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<vd_msgs::msg::VDstate_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<vd_msgs::msg::VDstate_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<vd_msgs::msg::VDstate_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__vd_msgs__msg__VDstate
    std::shared_ptr<vd_msgs::msg::VDstate_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__vd_msgs__msg__VDstate
    std::shared_ptr<vd_msgs::msg::VDstate_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const VDstate_ & other) const
  {
    if (this->vx != other.vx) {
      return false;
    }
    if (this->vy != other.vy) {
      return false;
    }
    if (this->r != other.r) {
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
    if (this->w_fl != other.w_fl) {
      return false;
    }
    if (this->w_fr != other.w_fr) {
      return false;
    }
    if (this->w_rl != other.w_rl) {
      return false;
    }
    if (this->w_rr != other.w_rr) {
      return false;
    }
    if (this->s != other.s) {
      return false;
    }
    return true;
  }
  bool operator!=(const VDstate_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct VDstate_

// alias to use template instance with default allocator
using VDstate =
  vd_msgs::msg::VDstate_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace vd_msgs

#endif  // VD_MSGS__MSG__DETAIL__V_DSTATE__STRUCT_HPP_
