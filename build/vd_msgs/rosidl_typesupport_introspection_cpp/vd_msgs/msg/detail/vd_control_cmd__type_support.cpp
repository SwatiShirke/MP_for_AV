// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from vd_msgs:msg/VDControlCMD.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "vd_msgs/msg/detail/vd_control_cmd__struct.hpp"
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

void VDControlCMD_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) vd_msgs::msg::VDControlCMD(_init);
}

void VDControlCMD_fini_function(void * message_memory)
{
  auto typed_message = static_cast<vd_msgs::msg::VDControlCMD *>(message_memory);
  typed_message->~VDControlCMD();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember VDControlCMD_message_member_array[2] = {
  {
    "velocity",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vd_msgs::msg::VDControlCMD, velocity),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "steering_angle",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vd_msgs::msg::VDControlCMD, steering_angle),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers VDControlCMD_message_members = {
  "vd_msgs::msg",  // message namespace
  "VDControlCMD",  // message name
  2,  // number of fields
  sizeof(vd_msgs::msg::VDControlCMD),
  VDControlCMD_message_member_array,  // message members
  VDControlCMD_init_function,  // function to initialize message memory (memory has to be allocated)
  VDControlCMD_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t VDControlCMD_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &VDControlCMD_message_members,
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
get_message_type_support_handle<vd_msgs::msg::VDControlCMD>()
{
  return &::vd_msgs::msg::rosidl_typesupport_introspection_cpp::VDControlCMD_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, vd_msgs, msg, VDControlCMD)() {
  return &::vd_msgs::msg::rosidl_typesupport_introspection_cpp::VDControlCMD_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
