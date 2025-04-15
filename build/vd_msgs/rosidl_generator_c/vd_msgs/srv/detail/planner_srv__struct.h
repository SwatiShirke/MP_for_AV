// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from vd_msgs:srv/PlannerSrv.idl
// generated code does not contain a copyright notice

#ifndef VD_MSGS__SRV__DETAIL__PLANNER_SRV__STRUCT_H_
#define VD_MSGS__SRV__DETAIL__PLANNER_SRV__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/PlannerSrv in the package vd_msgs.
typedef struct vd_msgs__srv__PlannerSrv_Request
{
  float x;
  float y;
} vd_msgs__srv__PlannerSrv_Request;

// Struct for a sequence of vd_msgs__srv__PlannerSrv_Request.
typedef struct vd_msgs__srv__PlannerSrv_Request__Sequence
{
  vd_msgs__srv__PlannerSrv_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} vd_msgs__srv__PlannerSrv_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/PlannerSrv in the package vd_msgs.
typedef struct vd_msgs__srv__PlannerSrv_Response
{
  rosidl_runtime_c__String message;
} vd_msgs__srv__PlannerSrv_Response;

// Struct for a sequence of vd_msgs__srv__PlannerSrv_Response.
typedef struct vd_msgs__srv__PlannerSrv_Response__Sequence
{
  vd_msgs__srv__PlannerSrv_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} vd_msgs__srv__PlannerSrv_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // VD_MSGS__SRV__DETAIL__PLANNER_SRV__STRUCT_H_
