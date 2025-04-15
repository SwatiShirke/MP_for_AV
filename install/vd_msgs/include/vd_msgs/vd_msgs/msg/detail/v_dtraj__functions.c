// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from vd_msgs:msg/VDtraj.idl
// generated code does not contain a copyright notice
#include "vd_msgs/msg/detail/v_dtraj__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `poses`
#include "vd_msgs/msg/detail/v_dpose__functions.h"

bool
vd_msgs__msg__VDtraj__init(vd_msgs__msg__VDtraj * msg)
{
  if (!msg) {
    return false;
  }
  // poses
  if (!vd_msgs__msg__VDpose__Sequence__init(&msg->poses, 0)) {
    vd_msgs__msg__VDtraj__fini(msg);
    return false;
  }
  return true;
}

void
vd_msgs__msg__VDtraj__fini(vd_msgs__msg__VDtraj * msg)
{
  if (!msg) {
    return;
  }
  // poses
  vd_msgs__msg__VDpose__Sequence__fini(&msg->poses);
}

bool
vd_msgs__msg__VDtraj__are_equal(const vd_msgs__msg__VDtraj * lhs, const vd_msgs__msg__VDtraj * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // poses
  if (!vd_msgs__msg__VDpose__Sequence__are_equal(
      &(lhs->poses), &(rhs->poses)))
  {
    return false;
  }
  return true;
}

bool
vd_msgs__msg__VDtraj__copy(
  const vd_msgs__msg__VDtraj * input,
  vd_msgs__msg__VDtraj * output)
{
  if (!input || !output) {
    return false;
  }
  // poses
  if (!vd_msgs__msg__VDpose__Sequence__copy(
      &(input->poses), &(output->poses)))
  {
    return false;
  }
  return true;
}

vd_msgs__msg__VDtraj *
vd_msgs__msg__VDtraj__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vd_msgs__msg__VDtraj * msg = (vd_msgs__msg__VDtraj *)allocator.allocate(sizeof(vd_msgs__msg__VDtraj), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(vd_msgs__msg__VDtraj));
  bool success = vd_msgs__msg__VDtraj__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
vd_msgs__msg__VDtraj__destroy(vd_msgs__msg__VDtraj * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    vd_msgs__msg__VDtraj__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
vd_msgs__msg__VDtraj__Sequence__init(vd_msgs__msg__VDtraj__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vd_msgs__msg__VDtraj * data = NULL;

  if (size) {
    data = (vd_msgs__msg__VDtraj *)allocator.zero_allocate(size, sizeof(vd_msgs__msg__VDtraj), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = vd_msgs__msg__VDtraj__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        vd_msgs__msg__VDtraj__fini(&data[i - 1]);
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
vd_msgs__msg__VDtraj__Sequence__fini(vd_msgs__msg__VDtraj__Sequence * array)
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
      vd_msgs__msg__VDtraj__fini(&array->data[i]);
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

vd_msgs__msg__VDtraj__Sequence *
vd_msgs__msg__VDtraj__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vd_msgs__msg__VDtraj__Sequence * array = (vd_msgs__msg__VDtraj__Sequence *)allocator.allocate(sizeof(vd_msgs__msg__VDtraj__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = vd_msgs__msg__VDtraj__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
vd_msgs__msg__VDtraj__Sequence__destroy(vd_msgs__msg__VDtraj__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    vd_msgs__msg__VDtraj__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
vd_msgs__msg__VDtraj__Sequence__are_equal(const vd_msgs__msg__VDtraj__Sequence * lhs, const vd_msgs__msg__VDtraj__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!vd_msgs__msg__VDtraj__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
vd_msgs__msg__VDtraj__Sequence__copy(
  const vd_msgs__msg__VDtraj__Sequence * input,
  vd_msgs__msg__VDtraj__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(vd_msgs__msg__VDtraj);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    vd_msgs__msg__VDtraj * data =
      (vd_msgs__msg__VDtraj *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!vd_msgs__msg__VDtraj__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          vd_msgs__msg__VDtraj__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!vd_msgs__msg__VDtraj__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
