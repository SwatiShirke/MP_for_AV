// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from vd_carla_msgs:msg/CarlaEgoVehicleControl.idl
// generated code does not contain a copyright notice

#ifndef VD_CARLA_MSGS__MSG__DETAIL__CARLA_EGO_VEHICLE_CONTROL__STRUCT_H_
#define VD_CARLA_MSGS__MSG__DETAIL__CARLA_EGO_VEHICLE_CONTROL__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"

/// Struct defined in msg/CarlaEgoVehicleControl in the package vd_carla_msgs.
/**
  * Copyright (c) 2018-2019 Intel Corporation.
  *
  * This work is licensed under the terms of the MIT license.
  * For a copy, see <https://opensource.org/licenses/MIT>.
  *
  * This represents a vehicle control message sent to CARLA simulator
 */
typedef struct vd_carla_msgs__msg__CarlaEgoVehicleControl
{
  std_msgs__msg__Header header;
  /// The CARLA vehicle control data
  /// 0. <= throttle <= 1.
  float throttle;
  /// -1. <= steer <= 1.
  float steer;
  /// 0. <= brake <= 1.
  float brake;
  /// hand_brake 0 or 1
  bool hand_brake;
  /// reverse 0 or 1
  bool reverse;
  /// gear
  int32_t gear;
  /// manual gear shift
  bool manual_gear_shift;
} vd_carla_msgs__msg__CarlaEgoVehicleControl;

// Struct for a sequence of vd_carla_msgs__msg__CarlaEgoVehicleControl.
typedef struct vd_carla_msgs__msg__CarlaEgoVehicleControl__Sequence
{
  vd_carla_msgs__msg__CarlaEgoVehicleControl * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} vd_carla_msgs__msg__CarlaEgoVehicleControl__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // VD_CARLA_MSGS__MSG__DETAIL__CARLA_EGO_VEHICLE_CONTROL__STRUCT_H_
