// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from vd_msgs:msg/VDList.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "vd_msgs/msg/detail/vd_list__rosidl_typesupport_introspection_c.h"
#include "vd_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "vd_msgs/msg/detail/vd_list__functions.h"
#include "vd_msgs/msg/detail/vd_list__struct.h"


// Include directives for member types
// Member `vdlist`
#include "vd_msgs/msg/vd_info.h"
// Member `vdlist`
#include "vd_msgs/msg/detail/vd_info__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void vd_msgs__msg__VDList__rosidl_typesupport_introspection_c__VDList_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  vd_msgs__msg__VDList__init(message_memory);
}

void vd_msgs__msg__VDList__rosidl_typesupport_introspection_c__VDList_fini_function(void * message_memory)
{
  vd_msgs__msg__VDList__fini(message_memory);
}

size_t vd_msgs__msg__VDList__rosidl_typesupport_introspection_c__size_function__VDList__vdlist(
  const void * untyped_member)
{
  const vd_msgs__msg__VDInfo__Sequence * member =
    (const vd_msgs__msg__VDInfo__Sequence *)(untyped_member);
  return member->size;
}

const void * vd_msgs__msg__VDList__rosidl_typesupport_introspection_c__get_const_function__VDList__vdlist(
  const void * untyped_member, size_t index)
{
  const vd_msgs__msg__VDInfo__Sequence * member =
    (const vd_msgs__msg__VDInfo__Sequence *)(untyped_member);
  return &member->data[index];
}

void * vd_msgs__msg__VDList__rosidl_typesupport_introspection_c__get_function__VDList__vdlist(
  void * untyped_member, size_t index)
{
  vd_msgs__msg__VDInfo__Sequence * member =
    (vd_msgs__msg__VDInfo__Sequence *)(untyped_member);
  return &member->data[index];
}

void vd_msgs__msg__VDList__rosidl_typesupport_introspection_c__fetch_function__VDList__vdlist(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const vd_msgs__msg__VDInfo * item =
    ((const vd_msgs__msg__VDInfo *)
    vd_msgs__msg__VDList__rosidl_typesupport_introspection_c__get_const_function__VDList__vdlist(untyped_member, index));
  vd_msgs__msg__VDInfo * value =
    (vd_msgs__msg__VDInfo *)(untyped_value);
  *value = *item;
}

void vd_msgs__msg__VDList__rosidl_typesupport_introspection_c__assign_function__VDList__vdlist(
  void * untyped_member, size_t index, const void * untyped_value)
{
  vd_msgs__msg__VDInfo * item =
    ((vd_msgs__msg__VDInfo *)
    vd_msgs__msg__VDList__rosidl_typesupport_introspection_c__get_function__VDList__vdlist(untyped_member, index));
  const vd_msgs__msg__VDInfo * value =
    (const vd_msgs__msg__VDInfo *)(untyped_value);
  *item = *value;
}

bool vd_msgs__msg__VDList__rosidl_typesupport_introspection_c__resize_function__VDList__vdlist(
  void * untyped_member, size_t size)
{
  vd_msgs__msg__VDInfo__Sequence * member =
    (vd_msgs__msg__VDInfo__Sequence *)(untyped_member);
  vd_msgs__msg__VDInfo__Sequence__fini(member);
  return vd_msgs__msg__VDInfo__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember vd_msgs__msg__VDList__rosidl_typesupport_introspection_c__VDList_message_member_array[1] = {
  {
    "vdlist",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vd_msgs__msg__VDList, vdlist),  // bytes offset in struct
    NULL,  // default value
    vd_msgs__msg__VDList__rosidl_typesupport_introspection_c__size_function__VDList__vdlist,  // size() function pointer
    vd_msgs__msg__VDList__rosidl_typesupport_introspection_c__get_const_function__VDList__vdlist,  // get_const(index) function pointer
    vd_msgs__msg__VDList__rosidl_typesupport_introspection_c__get_function__VDList__vdlist,  // get(index) function pointer
    vd_msgs__msg__VDList__rosidl_typesupport_introspection_c__fetch_function__VDList__vdlist,  // fetch(index, &value) function pointer
    vd_msgs__msg__VDList__rosidl_typesupport_introspection_c__assign_function__VDList__vdlist,  // assign(index, value) function pointer
    vd_msgs__msg__VDList__rosidl_typesupport_introspection_c__resize_function__VDList__vdlist  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers vd_msgs__msg__VDList__rosidl_typesupport_introspection_c__VDList_message_members = {
  "vd_msgs__msg",  // message namespace
  "VDList",  // message name
  1,  // number of fields
  sizeof(vd_msgs__msg__VDList),
  vd_msgs__msg__VDList__rosidl_typesupport_introspection_c__VDList_message_member_array,  // message members
  vd_msgs__msg__VDList__rosidl_typesupport_introspection_c__VDList_init_function,  // function to initialize message memory (memory has to be allocated)
  vd_msgs__msg__VDList__rosidl_typesupport_introspection_c__VDList_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t vd_msgs__msg__VDList__rosidl_typesupport_introspection_c__VDList_message_type_support_handle = {
  0,
  &vd_msgs__msg__VDList__rosidl_typesupport_introspection_c__VDList_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_vd_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, vd_msgs, msg, VDList)() {
  vd_msgs__msg__VDList__rosidl_typesupport_introspection_c__VDList_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, vd_msgs, msg, VDInfo)();
  if (!vd_msgs__msg__VDList__rosidl_typesupport_introspection_c__VDList_message_type_support_handle.typesupport_identifier) {
    vd_msgs__msg__VDList__rosidl_typesupport_introspection_c__VDList_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &vd_msgs__msg__VDList__rosidl_typesupport_introspection_c__VDList_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
