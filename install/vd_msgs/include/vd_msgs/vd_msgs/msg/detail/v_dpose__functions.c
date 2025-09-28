// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from vd_msgs:msg/VDpose.idl
// generated code does not contain a copyright notice
#include "vd_msgs/msg/detail/v_dpose__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"

bool
vd_msgs__msg__VDpose__init(vd_msgs__msg__VDpose * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    vd_msgs__msg__VDpose__fini(msg);
    return false;
  }
  // x
  // y
  // psi
  // velocity
  // distance
  // x_lane_center
  // y_lane_center
  // yaw_lane_center
  // total_distance
  // acceleration
  // steering_angle
  // length
  // width
  return true;
}

void
vd_msgs__msg__VDpose__fini(vd_msgs__msg__VDpose * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // x
  // y
  // psi
  // velocity
  // distance
  // x_lane_center
  // y_lane_center
  // yaw_lane_center
  // total_distance
  // acceleration
  // steering_angle
  // length
  // width
}

bool
vd_msgs__msg__VDpose__are_equal(const vd_msgs__msg__VDpose * lhs, const vd_msgs__msg__VDpose * rhs)
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
  // x
  if (lhs->x != rhs->x) {
    return false;
  }
  // y
  if (lhs->y != rhs->y) {
    return false;
  }
  // psi
  if (lhs->psi != rhs->psi) {
    return false;
  }
  // velocity
  if (lhs->velocity != rhs->velocity) {
    return false;
  }
  // distance
  if (lhs->distance != rhs->distance) {
    return false;
  }
  // x_lane_center
  if (lhs->x_lane_center != rhs->x_lane_center) {
    return false;
  }
  // y_lane_center
  if (lhs->y_lane_center != rhs->y_lane_center) {
    return false;
  }
  // yaw_lane_center
  if (lhs->yaw_lane_center != rhs->yaw_lane_center) {
    return false;
  }
  // total_distance
  if (lhs->total_distance != rhs->total_distance) {
    return false;
  }
  // acceleration
  if (lhs->acceleration != rhs->acceleration) {
    return false;
  }
  // steering_angle
  if (lhs->steering_angle != rhs->steering_angle) {
    return false;
  }
  // length
  if (lhs->length != rhs->length) {
    return false;
  }
  // width
  if (lhs->width != rhs->width) {
    return false;
  }
  return true;
}

bool
vd_msgs__msg__VDpose__copy(
  const vd_msgs__msg__VDpose * input,
  vd_msgs__msg__VDpose * output)
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
  // x
  output->x = input->x;
  // y
  output->y = input->y;
  // psi
  output->psi = input->psi;
  // velocity
  output->velocity = input->velocity;
  // distance
  output->distance = input->distance;
  // x_lane_center
  output->x_lane_center = input->x_lane_center;
  // y_lane_center
  output->y_lane_center = input->y_lane_center;
  // yaw_lane_center
  output->yaw_lane_center = input->yaw_lane_center;
  // total_distance
  output->total_distance = input->total_distance;
  // acceleration
  output->acceleration = input->acceleration;
  // steering_angle
  output->steering_angle = input->steering_angle;
  // length
  output->length = input->length;
  // width
  output->width = input->width;
  return true;
}

vd_msgs__msg__VDpose *
vd_msgs__msg__VDpose__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vd_msgs__msg__VDpose * msg = (vd_msgs__msg__VDpose *)allocator.allocate(sizeof(vd_msgs__msg__VDpose), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(vd_msgs__msg__VDpose));
  bool success = vd_msgs__msg__VDpose__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
vd_msgs__msg__VDpose__destroy(vd_msgs__msg__VDpose * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    vd_msgs__msg__VDpose__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
vd_msgs__msg__VDpose__Sequence__init(vd_msgs__msg__VDpose__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vd_msgs__msg__VDpose * data = NULL;

  if (size) {
    data = (vd_msgs__msg__VDpose *)allocator.zero_allocate(size, sizeof(vd_msgs__msg__VDpose), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = vd_msgs__msg__VDpose__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        vd_msgs__msg__VDpose__fini(&data[i - 1]);
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
vd_msgs__msg__VDpose__Sequence__fini(vd_msgs__msg__VDpose__Sequence * array)
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
      vd_msgs__msg__VDpose__fini(&array->data[i]);
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

vd_msgs__msg__VDpose__Sequence *
vd_msgs__msg__VDpose__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vd_msgs__msg__VDpose__Sequence * array = (vd_msgs__msg__VDpose__Sequence *)allocator.allocate(sizeof(vd_msgs__msg__VDpose__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = vd_msgs__msg__VDpose__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
vd_msgs__msg__VDpose__Sequence__destroy(vd_msgs__msg__VDpose__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    vd_msgs__msg__VDpose__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
vd_msgs__msg__VDpose__Sequence__are_equal(const vd_msgs__msg__VDpose__Sequence * lhs, const vd_msgs__msg__VDpose__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!vd_msgs__msg__VDpose__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
vd_msgs__msg__VDpose__Sequence__copy(
  const vd_msgs__msg__VDpose__Sequence * input,
  vd_msgs__msg__VDpose__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(vd_msgs__msg__VDpose);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    vd_msgs__msg__VDpose * data =
      (vd_msgs__msg__VDpose *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!vd_msgs__msg__VDpose__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          vd_msgs__msg__VDpose__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!vd_msgs__msg__VDpose__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
