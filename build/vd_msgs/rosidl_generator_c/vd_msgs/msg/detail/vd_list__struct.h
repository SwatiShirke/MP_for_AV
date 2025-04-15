// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from vd_msgs:msg/VDList.idl
// generated code does not contain a copyright notice

#ifndef VD_MSGS__MSG__DETAIL__VD_LIST__STRUCT_H_
#define VD_MSGS__MSG__DETAIL__VD_LIST__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'vdlist'
#include "vd_msgs/msg/detail/vd_info__struct.h"

/// Struct defined in msg/VDList in the package vd_msgs.
typedef struct vd_msgs__msg__VDList
{
  vd_msgs__msg__VDInfo__Sequence vdlist;
} vd_msgs__msg__VDList;

// Struct for a sequence of vd_msgs__msg__VDList.
typedef struct vd_msgs__msg__VDList__Sequence
{
  vd_msgs__msg__VDList * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} vd_msgs__msg__VDList__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // VD_MSGS__MSG__DETAIL__VD_LIST__STRUCT_H_
