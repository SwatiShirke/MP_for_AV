// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from vd_msgs:msg/VDPath.idl
// generated code does not contain a copyright notice
#include "vd_msgs/msg/detail/vd_path__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `x_val`
// Member `y_val`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
vd_msgs__msg__VDPath__init(vd_msgs__msg__VDPath * msg)
{
  if (!msg) {
    return false;
  }
  // x_val
  if (!rosidl_runtime_c__float__Sequence__init(&msg->x_val, 0)) {
    vd_msgs__msg__VDPath__fini(msg);
    return false;
  }
  // y_val
  if (!rosidl_runtime_c__float__Sequence__init(&msg->y_val, 0)) {
    vd_msgs__msg__VDPath__fini(msg);
    return false;
  }
  return true;
}

void
vd_msgs__msg__VDPath__fini(vd_msgs__msg__VDPath * msg)
{
  if (!msg) {
    return;
  }
  // x_val
  rosidl_runtime_c__float__Sequence__fini(&msg->x_val);
  // y_val
  rosidl_runtime_c__float__Sequence__fini(&msg->y_val);
}

bool
vd_msgs__msg__VDPath__are_equal(const vd_msgs__msg__VDPath * lhs, const vd_msgs__msg__VDPath * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // x_val
  if (!rosidl_runtime_c__float__Sequence__are_equal(
      &(lhs->x_val), &(rhs->x_val)))
  {
    return false;
  }
  // y_val
  if (!rosidl_runtime_c__float__Sequence__are_equal(
      &(lhs->y_val), &(rhs->y_val)))
  {
    return false;
  }
  return true;
}

bool
vd_msgs__msg__VDPath__copy(
  const vd_msgs__msg__VDPath * input,
  vd_msgs__msg__VDPath * output)
{
  if (!input || !output) {
    return false;
  }
  // x_val
  if (!rosidl_runtime_c__float__Sequence__copy(
      &(input->x_val), &(output->x_val)))
  {
    return false;
  }
  // y_val
  if (!rosidl_runtime_c__float__Sequence__copy(
      &(input->y_val), &(output->y_val)))
  {
    return false;
  }
  return true;
}

vd_msgs__msg__VDPath *
vd_msgs__msg__VDPath__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vd_msgs__msg__VDPath * msg = (vd_msgs__msg__VDPath *)allocator.allocate(sizeof(vd_msgs__msg__VDPath), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(vd_msgs__msg__VDPath));
  bool success = vd_msgs__msg__VDPath__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
vd_msgs__msg__VDPath__destroy(vd_msgs__msg__VDPath * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    vd_msgs__msg__VDPath__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
vd_msgs__msg__VDPath__Sequence__init(vd_msgs__msg__VDPath__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vd_msgs__msg__VDPath * data = NULL;

  if (size) {
    data = (vd_msgs__msg__VDPath *)allocator.zero_allocate(size, sizeof(vd_msgs__msg__VDPath), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = vd_msgs__msg__VDPath__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        vd_msgs__msg__VDPath__fini(&data[i - 1]);
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
vd_msgs__msg__VDPath__Sequence__fini(vd_msgs__msg__VDPath__Sequence * array)
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
      vd_msgs__msg__VDPath__fini(&array->data[i]);
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

vd_msgs__msg__VDPath__Sequence *
vd_msgs__msg__VDPath__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vd_msgs__msg__VDPath__Sequence * array = (vd_msgs__msg__VDPath__Sequence *)allocator.allocate(sizeof(vd_msgs__msg__VDPath__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = vd_msgs__msg__VDPath__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
vd_msgs__msg__VDPath__Sequence__destroy(vd_msgs__msg__VDPath__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    vd_msgs__msg__VDPath__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
vd_msgs__msg__VDPath__Sequence__are_equal(const vd_msgs__msg__VDPath__Sequence * lhs, const vd_msgs__msg__VDPath__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!vd_msgs__msg__VDPath__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
vd_msgs__msg__VDPath__Sequence__copy(
  const vd_msgs__msg__VDPath__Sequence * input,
  vd_msgs__msg__VDPath__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(vd_msgs__msg__VDPath);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    vd_msgs__msg__VDPath * data =
      (vd_msgs__msg__VDPath *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!vd_msgs__msg__VDPath__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          vd_msgs__msg__VDPath__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!vd_msgs__msg__VDPath__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
