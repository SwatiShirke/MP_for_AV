// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from vd_msgs:msg/VDPath.idl
// generated code does not contain a copyright notice

#ifndef VD_MSGS__MSG__DETAIL__VD_PATH__STRUCT_H_
#define VD_MSGS__MSG__DETAIL__VD_PATH__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'x_val'
// Member 'y_val'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in msg/VDPath in the package vd_msgs.
typedef struct vd_msgs__msg__VDPath
{
  rosidl_runtime_c__float__Sequence x_val;
  rosidl_runtime_c__float__Sequence y_val;
} vd_msgs__msg__VDPath;

// Struct for a sequence of vd_msgs__msg__VDPath.
typedef struct vd_msgs__msg__VDPath__Sequence
{
  vd_msgs__msg__VDPath * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} vd_msgs__msg__VDPath__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // VD_MSGS__MSG__DETAIL__VD_PATH__STRUCT_H_
