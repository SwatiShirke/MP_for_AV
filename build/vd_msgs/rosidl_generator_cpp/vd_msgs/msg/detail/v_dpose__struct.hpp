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


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"

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
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->x = 0.0;
      this->y = 0.0;
      this->psi = 0.0;
      this->velocity = 0.0;
      this->distance = 0.0;
      this->x_lane_center = 0.0;
      this->y_lane_center = 0.0;
      this->yaw_lane_center = 0.0;
      this->total_distance = 0.0;
      this->acceleration = 0.0;
      this->steering_angle = 0.0;
      this->length = 0.0;
      this->width = 0.0;
    }
  }

  explicit VDpose_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->x = 0.0;
      this->y = 0.0;
      this->psi = 0.0;
      this->velocity = 0.0;
      this->distance = 0.0;
      this->x_lane_center = 0.0;
      this->y_lane_center = 0.0;
      this->yaw_lane_center = 0.0;
      this->total_distance = 0.0;
      this->acceleration = 0.0;
      this->steering_angle = 0.0;
      this->length = 0.0;
      this->width = 0.0;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _x_type =
    double;
  _x_type x;
  using _y_type =
    double;
  _y_type y;
  using _psi_type =
    double;
  _psi_type psi;
  using _velocity_type =
    double;
  _velocity_type velocity;
  using _distance_type =
    double;
  _distance_type distance;
  using _x_lane_center_type =
    double;
  _x_lane_center_type x_lane_center;
  using _y_lane_center_type =
    double;
  _y_lane_center_type y_lane_center;
  using _yaw_lane_center_type =
    double;
  _yaw_lane_center_type yaw_lane_center;
  using _total_distance_type =
    double;
  _total_distance_type total_distance;
  using _acceleration_type =
    double;
  _acceleration_type acceleration;
  using _steering_angle_type =
    double;
  _steering_angle_type steering_angle;
  using _length_type =
    double;
  _length_type length;
  using _width_type =
    double;
  _width_type width;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
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
  Type & set__velocity(
    const double & _arg)
  {
    this->velocity = _arg;
    return *this;
  }
  Type & set__distance(
    const double & _arg)
  {
    this->distance = _arg;
    return *this;
  }
  Type & set__x_lane_center(
    const double & _arg)
  {
    this->x_lane_center = _arg;
    return *this;
  }
  Type & set__y_lane_center(
    const double & _arg)
  {
    this->y_lane_center = _arg;
    return *this;
  }
  Type & set__yaw_lane_center(
    const double & _arg)
  {
    this->yaw_lane_center = _arg;
    return *this;
  }
  Type & set__total_distance(
    const double & _arg)
  {
    this->total_distance = _arg;
    return *this;
  }
  Type & set__acceleration(
    const double & _arg)
  {
    this->acceleration = _arg;
    return *this;
  }
  Type & set__steering_angle(
    const double & _arg)
  {
    this->steering_angle = _arg;
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
    if (this->header != other.header) {
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
    if (this->velocity != other.velocity) {
      return false;
    }
    if (this->distance != other.distance) {
      return false;
    }
    if (this->x_lane_center != other.x_lane_center) {
      return false;
    }
    if (this->y_lane_center != other.y_lane_center) {
      return false;
    }
    if (this->yaw_lane_center != other.yaw_lane_center) {
      return false;
    }
    if (this->total_distance != other.total_distance) {
      return false;
    }
    if (this->acceleration != other.acceleration) {
      return false;
    }
    if (this->steering_angle != other.steering_angle) {
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
