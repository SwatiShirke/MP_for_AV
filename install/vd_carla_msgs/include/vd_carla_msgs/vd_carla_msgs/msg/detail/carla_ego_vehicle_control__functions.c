// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from vd_carla_msgs:msg/CarlaEgoVehicleControl.idl
// generated code does not contain a copyright notice
#include "vd_carla_msgs/msg/detail/carla_ego_vehicle_control__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"

bool
vd_carla_msgs__msg__CarlaEgoVehicleControl__init(vd_carla_msgs__msg__CarlaEgoVehicleControl * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    vd_carla_msgs__msg__CarlaEgoVehicleControl__fini(msg);
    return false;
  }
  // throttle
  // steer
  // brake
  // hand_brake
  // reverse
  // gear
  // manual_gear_shift
  return true;
}

void
vd_carla_msgs__msg__CarlaEgoVehicleControl__fini(vd_carla_msgs__msg__CarlaEgoVehicleControl * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // throttle
  // steer
  // brake
  // hand_brake
  // reverse
  // gear
  // manual_gear_shift
}

bool
vd_carla_msgs__msg__CarlaEgoVehicleControl__are_equal(const vd_carla_msgs__msg__CarlaEgoVehicleControl * lhs, const vd_carla_msgs__msg__CarlaEgoVehicleControl * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // throttle
  if (lhs->throttle != rhs->throttle) {
    return false;
  }
  // steer
  if (lhs->steer != rhs->steer) {
    return false;
  }
  // brake
  if (lhs->brake != rhs->brake) {
    return false;
  }
  // hand_brake
  if (lhs->hand_brake != rhs->hand_brake) {
    return false;
  }
  // reverse
  if (lhs->reverse != rhs->reverse) {
    return false;
  }
  // gear
  if (lhs->gear != rhs->gear) {
    return false;
  }
  // manual_gear_shift
  if (lhs->manual_gear_shift != rhs->manual_gear_shift) {
    return false;
  }
  return true;
}

bool
vd_carla_msgs__msg__CarlaEgoVehicleControl__copy(
  const vd_carla_msgs__msg__CarlaEgoVehicleControl * input,
  vd_carla_msgs__msg__CarlaEgoVehicleControl * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // throttle
  output->throttle = input->throttle;
  // steer
  output->steer = input->steer;
  // brake
  output->brake = input->brake;
  // hand_brake
  output->hand_brake = input->hand_brake;
  // reverse
  output->reverse = input->reverse;
  // gear
  output->gear = input->gear;
  // manual_gear_shift
  output->manual_gear_shift = input->manual_gear_shift;
  return true;
}

vd_carla_msgs__msg__CarlaEgoVehicleControl *
vd_carla_msgs__msg__CarlaEgoVehicleControl__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vd_carla_msgs__msg__CarlaEgoVehicleControl * msg = (vd_carla_msgs__msg__CarlaEgoVehicleControl *)allocator.allocate(sizeof(vd_carla_msgs__msg__CarlaEgoVehicleControl), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(vd_carla_msgs__msg__CarlaEgoVehicleControl));
  bool success = vd_carla_msgs__msg__CarlaEgoVehicleControl__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
vd_carla_msgs__msg__CarlaEgoVehicleControl__destroy(vd_carla_msgs__msg__CarlaEgoVehicleControl * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    vd_carla_msgs__msg__CarlaEgoVehicleControl__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
vd_carla_msgs__msg__CarlaEgoVehicleControl__Sequence__init(vd_carla_msgs__msg__CarlaEgoVehicleControl__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vd_carla_msgs__msg__CarlaEgoVehicleControl * data = NULL;

  if (size) {
    data = (vd_carla_msgs__msg__CarlaEgoVehicleControl *)allocator.zero_allocate(size, sizeof(vd_carla_msgs__msg__CarlaEgoVehicleControl), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = vd_carla_msgs__msg__CarlaEgoVehicleControl__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        vd_carla_msgs__msg__CarlaEgoVehicleControl__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
vd_carla_msgs__msg__CarlaEgoVehicleControl__Sequence__fini(vd_carla_msgs__msg__CarlaEgoVehicleControl__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      vd_carla_msgs__msg__CarlaEgoVehicleControl__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

vd_carla_msgs__msg__CarlaEgoVehicleControl__Sequence *
vd_carla_msgs__msg__CarlaEgoVehicleControl__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vd_carla_msgs__msg__CarlaEgoVehicleControl__Sequence * array = (vd_carla_msgs__msg__CarlaEgoVehicleControl__Sequence *)allocator.allocate(sizeof(vd_carla_msgs__msg__CarlaEgoVehicleControl__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = vd_carla_msgs__msg__CarlaEgoVehicleControl__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
vd_carla_msgs__msg__CarlaEgoVehicleControl__Sequence__destroy(vd_carla_msgs__msg__CarlaEgoVehicleControl__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    vd_carla_msgs__msg__CarlaEgoVehicleControl__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
vd_carla_msgs__msg__CarlaEgoVehicleControl__Sequence__are_equal(const vd_carla_msgs__msg__CarlaEgoVehicleControl__Sequence * lhs, const vd_carla_msgs__msg__CarlaEgoVehicleControl__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!vd_carla_msgs__msg__CarlaEgoVehicleControl__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
vd_carla_msgs__msg__CarlaEgoVehicleControl__Sequence__copy(
  const vd_carla_msgs__msg__CarlaEgoVehicleControl__Sequence * input,
  vd_carla_msgs__msg__CarlaEgoVehicleControl__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(vd_carla_msgs__msg__CarlaEgoVehicleControl);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    vd_carla_msgs__msg__CarlaEgoVehicleControl * data =
      (vd_carla_msgs__msg__CarlaEgoVehicleControl *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!vd_carla_msgs__msg__CarlaEgoVehicleControl__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          vd_carla_msgs__msg__CarlaEgoVehicleControl__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!vd_carla_msgs__msg__CarlaEgoVehicleControl__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
