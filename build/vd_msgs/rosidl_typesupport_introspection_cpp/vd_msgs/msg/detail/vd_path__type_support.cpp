// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from vd_msgs:msg/VDPath.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "vd_msgs/msg/detail/vd_path__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace vd_msgs
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void VDPath_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) vd_msgs::msg::VDPath(_init);
}

void VDPath_fini_function(void * message_memory)
{
  auto typed_message = static_cast<vd_msgs::msg::VDPath *>(message_memory);
  typed_message->~VDPath();
}

size_t size_function__VDPath__x_val(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<float> *>(untyped_member);
  return member->size();
}

const void * get_const_function__VDPath__x_val(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<float> *>(untyped_member);
  return &member[index];
}

void * get_function__VDPath__x_val(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<float> *>(untyped_member);
  return &member[index];
}

void fetch_function__VDPath__x_val(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const float *>(
    get_const_function__VDPath__x_val(untyped_member, index));
  auto & value = *reinterpret_cast<float *>(untyped_value);
  value = item;
}

void assign_function__VDPath__x_val(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<float *>(
    get_function__VDPath__x_val(untyped_member, index));
  const auto & value = *reinterpret_cast<const float *>(untyped_value);
  item = value;
}

void resize_function__VDPath__x_val(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<float> *>(untyped_member);
  member->resize(size);
}

size_t size_function__VDPath__y_val(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<float> *>(untyped_member);
  return member->size();
}

const void * get_const_function__VDPath__y_val(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<float> *>(untyped_member);
  return &member[index];
}

void * get_function__VDPath__y_val(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<float> *>(untyped_member);
  return &member[index];
}

void fetch_function__VDPath__y_val(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const float *>(
    get_const_function__VDPath__y_val(untyped_member, index));
  auto & value = *reinterpret_cast<float *>(untyped_value);
  value = item;
}

void assign_function__VDPath__y_val(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<float *>(
    get_function__VDPath__y_val(untyped_member, index));
  const auto & value = *reinterpret_cast<const float *>(untyped_value);
  item = value;
}

void resize_function__VDPath__y_val(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<float> *>(untyped_member);
  member->resize(size);
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember VDPath_message_member_array[2] = {
  {
    "x_val",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vd_msgs::msg::VDPath, x_val),  // bytes offset in struct
    nullptr,  // default value
    size_function__VDPath__x_val,  // size() function pointer
    get_const_function__VDPath__x_val,  // get_const(index) function pointer
    get_function__VDPath__x_val,  // get(index) function pointer
    fetch_function__VDPath__x_val,  // fetch(index, &value) function pointer
    assign_function__VDPath__x_val,  // assign(index, value) function pointer
    resize_function__VDPath__x_val  // resize(index) function pointer
  },
  {
    "y_val",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vd_msgs::msg::VDPath, y_val),  // bytes offset in struct
    nullptr,  // default value
    size_function__VDPath__y_val,  // size() function pointer
    get_const_function__VDPath__y_val,  // get_const(index) function pointer
    get_function__VDPath__y_val,  // get(index) function pointer
    fetch_function__VDPath__y_val,  // fetch(index, &value) function pointer
    assign_function__VDPath__y_val,  // assign(index, value) function pointer
    resize_function__VDPath__y_val  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers VDPath_message_members = {
  "vd_msgs::msg",  // message namespace
  "VDPath",  // message name
  2,  // number of fields
  sizeof(vd_msgs::msg::VDPath),
  VDPath_message_member_array,  // message members
  VDPath_init_function,  // function to initialize message memory (memory has to be allocated)
  VDPath_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t VDPath_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &VDPath_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace vd_msgs


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<vd_msgs::msg::VDPath>()
{
  return &::vd_msgs::msg::rosidl_typesupport_introspection_cpp::VDPath_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, vd_msgs, msg, VDPath)() {
  return &::vd_msgs::msg::rosidl_typesupport_introspection_cpp::VDPath_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
