// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from vd_msgs:msg/VDpose.idl
// generated code does not contain a copyright notice

#ifndef VD_MSGS__MSG__DETAIL__V_DPOSE__STRUCT_H_
#define VD_MSGS__MSG__DETAIL__V_DPOSE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/VDpose in the package vd_msgs.
typedef struct vd_msgs__msg__VDpose
{
  double s;
  double x;
  double y;
  double psi;
  double vf;
} vd_msgs__msg__VDpose;

// Struct for a sequence of vd_msgs__msg__VDpose.
typedef struct vd_msgs__msg__VDpose__Sequence
{
  vd_msgs__msg__VDpose * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} vd_msgs__msg__VDpose__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // VD_MSGS__MSG__DETAIL__V_DPOSE__STRUCT_H_
