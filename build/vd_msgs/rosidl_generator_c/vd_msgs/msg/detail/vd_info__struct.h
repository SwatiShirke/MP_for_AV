// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from vd_msgs:msg/VDInfo.idl
// generated code does not contain a copyright notice

#ifndef VD_MSGS__MSG__DETAIL__VD_INFO__STRUCT_H_
#define VD_MSGS__MSG__DETAIL__VD_INFO__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/VDInfo in the package vd_msgs.
typedef struct vd_msgs__msg__VDInfo
{
  double x;
  double y;
  double yaw;
  double length;
  double width;
} vd_msgs__msg__VDInfo;

// Struct for a sequence of vd_msgs__msg__VDInfo.
typedef struct vd_msgs__msg__VDInfo__Sequence
{
  vd_msgs__msg__VDInfo * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} vd_msgs__msg__VDInfo__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // VD_MSGS__MSG__DETAIL__VD_INFO__STRUCT_H_
