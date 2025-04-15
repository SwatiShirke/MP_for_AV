// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from vd_msgs:msg/VDstate.idl
// generated code does not contain a copyright notice

#ifndef VD_MSGS__MSG__DETAIL__V_DSTATE__STRUCT_H_
#define VD_MSGS__MSG__DETAIL__V_DSTATE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/VDstate in the package vd_msgs.
typedef struct vd_msgs__msg__VDstate
{
  double vx;
  double vy;
  double r;
  double x;
  double y;
  double psi;
  double w_fl;
  double w_fr;
  double w_rl;
  double w_rr;
  double s;
} vd_msgs__msg__VDstate;

// Struct for a sequence of vd_msgs__msg__VDstate.
typedef struct vd_msgs__msg__VDstate__Sequence
{
  vd_msgs__msg__VDstate * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} vd_msgs__msg__VDstate__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // VD_MSGS__MSG__DETAIL__V_DSTATE__STRUCT_H_
