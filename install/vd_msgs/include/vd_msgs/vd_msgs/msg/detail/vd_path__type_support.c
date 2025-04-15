// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from vd_msgs:msg/VDPath.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "vd_msgs/msg/detail/vd_path__rosidl_typesupport_introspection_c.h"
#include "vd_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "vd_msgs/msg/detail/vd_path__functions.h"
#include "vd_msgs/msg/detail/vd_path__struct.h"


// Include directives for member types
// Member `x_val`
// Member `y_val`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__VDPath_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  vd_msgs__msg__VDPath__init(message_memory);
}

void vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__VDPath_fini_function(void * message_memory)
{
  vd_msgs__msg__VDPath__fini(message_memory);
}

size_t vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__size_function__VDPath__x_val(
  const void * untyped_member)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return member->size;
}

const void * vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__get_const_function__VDPath__x_val(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void * vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__get_function__VDPath__x_val(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__fetch_function__VDPath__x_val(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__get_const_function__VDPath__x_val(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__assign_function__VDPath__x_val(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__get_function__VDPath__x_val(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

bool vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__resize_function__VDPath__x_val(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  rosidl_runtime_c__float__Sequence__fini(member);
  return rosidl_runtime_c__float__Sequence__init(member, size);
}

size_t vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__size_function__VDPath__y_val(
  const void * untyped_member)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return member->size;
}

const void * vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__get_const_function__VDPath__y_val(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void * vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__get_function__VDPath__y_val(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__fetch_function__VDPath__y_val(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__get_const_function__VDPath__y_val(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__assign_function__VDPath__y_val(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__get_function__VDPath__y_val(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

bool vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__resize_function__VDPath__y_val(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  rosidl_runtime_c__float__Sequence__fini(member);
  return rosidl_runtime_c__float__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__VDPath_message_member_array[2] = {
  {
    "x_val",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vd_msgs__msg__VDPath, x_val),  // bytes offset in struct
    NULL,  // default value
    vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__size_function__VDPath__x_val,  // size() function pointer
    vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__get_const_function__VDPath__x_val,  // get_const(index) function pointer
    vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__get_function__VDPath__x_val,  // get(index) function pointer
    vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__fetch_function__VDPath__x_val,  // fetch(index, &value) function pointer
    vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__assign_function__VDPath__x_val,  // assign(index, value) function pointer
    vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__resize_function__VDPath__x_val  // resize(index) function pointer
  },
  {
    "y_val",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vd_msgs__msg__VDPath, y_val),  // bytes offset in struct
    NULL,  // default value
    vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__size_function__VDPath__y_val,  // size() function pointer
    vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__get_const_function__VDPath__y_val,  // get_const(index) function pointer
    vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__get_function__VDPath__y_val,  // get(index) function pointer
    vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__fetch_function__VDPath__y_val,  // fetch(index, &value) function pointer
    vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__assign_function__VDPath__y_val,  // assign(index, value) function pointer
    vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__resize_function__VDPath__y_val  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__VDPath_message_members = {
  "vd_msgs__msg",  // message namespace
  "VDPath",  // message name
  2,  // number of fields
  sizeof(vd_msgs__msg__VDPath),
  vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__VDPath_message_member_array,  // message members
  vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__VDPath_init_function,  // function to initialize message memory (memory has to be allocated)
  vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__VDPath_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__VDPath_message_type_support_handle = {
  0,
  &vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__VDPath_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_vd_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, vd_msgs, msg, VDPath)() {
  if (!vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__VDPath_message_type_support_handle.typesupport_identifier) {
    vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__VDPath_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &vd_msgs__msg__VDPath__rosidl_typesupport_introspection_c__VDPath_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
