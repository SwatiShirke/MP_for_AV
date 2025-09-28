// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from vd_msgs:msg/VDtraj.idl
// generated code does not contain a copyright notice

#ifndef VD_MSGS__MSG__DETAIL__V_DTRAJ__STRUCT_HPP_
#define VD_MSGS__MSG__DETAIL__V_DTRAJ__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'poses'
#include "vd_msgs/msg/detail/v_dpose__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__vd_msgs__msg__VDtraj __attribute__((deprecated))
#else
# define DEPRECATED__vd_msgs__msg__VDtraj __declspec(deprecated)
#endif

namespace vd_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct VDtraj_
{
  using Type = VDtraj_<ContainerAllocator>;

  explicit VDtraj_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
  }

  explicit VDtraj_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
    (void)_alloc;
  }

  // field types and members
  using _poses_type =
    std::vector<vd_msgs::msg::VDpose_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<vd_msgs::msg::VDpose_<ContainerAllocator>>>;
  _poses_type poses;

  // setters for named parameter idiom
  Type & set__poses(
    const std::vector<vd_msgs::msg::VDpose_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<vd_msgs::msg::VDpose_<ContainerAllocator>>> & _arg)
  {
    this->poses = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    vd_msgs::msg::VDtraj_<ContainerAllocator> *;
  using ConstRawPtr =
    const vd_msgs::msg::VDtraj_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<vd_msgs::msg::VDtraj_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<vd_msgs::msg::VDtraj_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      vd_msgs::msg::VDtraj_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<vd_msgs::msg::VDtraj_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      vd_msgs::msg::VDtraj_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<vd_msgs::msg::VDtraj_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<vd_msgs::msg::VDtraj_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<vd_msgs::msg::VDtraj_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__vd_msgs__msg__VDtraj
    std::shared_ptr<vd_msgs::msg::VDtraj_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__vd_msgs__msg__VDtraj
    std::shared_ptr<vd_msgs::msg::VDtraj_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const VDtraj_ & other) const
  {
    if (this->poses != other.poses) {
      return false;
    }
    return true;
  }
  bool operator!=(const VDtraj_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct VDtraj_

// alias to use template instance with default allocator
using VDtraj =
  vd_msgs::msg::VDtraj_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace vd_msgs

#endif  // VD_MSGS__MSG__DETAIL__V_DTRAJ__STRUCT_HPP_
