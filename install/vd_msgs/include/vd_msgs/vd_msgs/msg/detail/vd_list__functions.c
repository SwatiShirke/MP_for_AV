// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from vd_msgs:msg/VDList.idl
// generated code does not contain a copyright notice
#include "vd_msgs/msg/detail/vd_list__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `vdlist`
#include "vd_msgs/msg/detail/vd_info__functions.h"

bool
vd_msgs__msg__VDList__init(vd_msgs__msg__VDList * msg)
{
  if (!msg) {
    return false;
  }
  // vdlist
  if (!vd_msgs__msg__VDInfo__Sequence__init(&msg->vdlist, 0)) {
    vd_msgs__msg__VDList__fini(msg);
    return false;
  }
  return true;
}

void
vd_msgs__msg__VDList__fini(vd_msgs__msg__VDList * msg)
{
  if (!msg) {
    return;
  }
  // vdlist
  vd_msgs__msg__VDInfo__Sequence__fini(&msg->vdlist);
}

bool
vd_msgs__msg__VDList__are_equal(const vd_msgs__msg__VDList * lhs, const vd_msgs__msg__VDList * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // vdlist
  if (!vd_msgs__msg__VDInfo__Sequence__are_equal(
      &(lhs->vdlist), &(rhs->vdlist)))
  {
    return false;
  }
  return true;
}

bool
vd_msgs__msg__VDList__copy(
  const vd_msgs__msg__VDList * input,
  vd_msgs__msg__VDList * output)
{
  if (!input || !output) {
    return false;
  }
  // vdlist
  if (!vd_msgs__msg__VDInfo__Sequence__copy(
      &(input->vdlist), &(output->vdlist)))
  {
    return false;
  }
  return true;
}

vd_msgs__msg__VDList *
vd_msgs__msg__VDList__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vd_msgs__msg__VDList * msg = (vd_msgs__msg__VDList *)allocator.allocate(sizeof(vd_msgs__msg__VDList), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(vd_msgs__msg__VDList));
  bool success = vd_msgs__msg__VDList__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
vd_msgs__msg__VDList__destroy(vd_msgs__msg__VDList * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    vd_msgs__msg__VDList__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
vd_msgs__msg__VDList__Sequence__init(vd_msgs__msg__VDList__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vd_msgs__msg__VDList * data = NULL;

  if (size) {
    data = (vd_msgs__msg__VDList *)allocator.zero_allocate(size, sizeof(vd_msgs__msg__VDList), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = vd_msgs__msg__VDList__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        vd_msgs__msg__VDList__fini(&data[i - 1]);
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
vd_msgs__msg__VDList__Sequence__fini(vd_msgs__msg__VDList__Sequence * array)
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
      vd_msgs__msg__VDList__fini(&array->data[i]);
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

vd_msgs__msg__VDList__Sequence *
vd_msgs__msg__VDList__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vd_msgs__msg__VDList__Sequence * array = (vd_msgs__msg__VDList__Sequence *)allocator.allocate(sizeof(vd_msgs__msg__VDList__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = vd_msgs__msg__VDList__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
vd_msgs__msg__VDList__Sequence__destroy(vd_msgs__msg__VDList__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    vd_msgs__msg__VDList__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
vd_msgs__msg__VDList__Sequence__are_equal(const vd_msgs__msg__VDList__Sequence * lhs, const vd_msgs__msg__VDList__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!vd_msgs__msg__VDList__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
vd_msgs__msg__VDList__Sequence__copy(
  const vd_msgs__msg__VDList__Sequence * input,
  vd_msgs__msg__VDList__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(vd_msgs__msg__VDList);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    vd_msgs__msg__VDList * data =
      (vd_msgs__msg__VDList *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!vd_msgs__msg__VDList__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          vd_msgs__msg__VDList__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!vd_msgs__msg__VDList__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
