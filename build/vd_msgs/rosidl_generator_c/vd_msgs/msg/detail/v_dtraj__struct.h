// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from vd_msgs:msg/VDtraj.idl
// generated code does not contain a copyright notice

#ifndef VD_MSGS__MSG__DETAIL__V_DTRAJ__STRUCT_H_
#define VD_MSGS__MSG__DETAIL__V_DTRAJ__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'poses'
#include "vd_msgs/msg/detail/v_dpose__struct.h"

/// Struct defined in msg/VDtraj in the package vd_msgs.
typedef struct vd_msgs__msg__VDtraj
{
  vd_msgs__msg__VDpose__Sequence poses;
} vd_msgs__msg__VDtraj;

// Struct for a sequence of vd_msgs__msg__VDtraj.
typedef struct vd_msgs__msg__VDtraj__Sequence
{
  vd_msgs__msg__VDtraj * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} vd_msgs__msg__VDtraj__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // VD_MSGS__MSG__DETAIL__V_DTRAJ__STRUCT_H_
