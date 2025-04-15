// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from vd_msgs:msg/VDstate.idl
// generated code does not contain a copyright notice
#include "vd_msgs/msg/detail/v_dstate__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
vd_msgs__msg__VDstate__init(vd_msgs__msg__VDstate * msg)
{
  if (!msg) {
    return false;
  }
  // vx
  // vy
  // r
  // x
  // y
  // psi
  // w_fl
  // w_fr
  // w_rl
  // w_rr
  // s
  return true;
}

void
vd_msgs__msg__VDstate__fini(vd_msgs__msg__VDstate * msg)
{
  if (!msg) {
    return;
  }
  // vx
  // vy
  // r
  // x
  // y
  // psi
  // w_fl
  // w_fr
  // w_rl
  // w_rr
  // s
}

bool
vd_msgs__msg__VDstate__are_equal(const vd_msgs__msg__VDstate * lhs, const vd_msgs__msg__VDstate * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // vx
  if (lhs->vx != rhs->vx) {
    return false;
  }
  // vy
  if (lhs->vy != rhs->vy) {
    return false;
  }
  // r
  if (lhs->r != rhs->r) {
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
  // w_fl
  if (lhs->w_fl != rhs->w_fl) {
    return false;
  }
  // w_fr
  if (lhs->w_fr != rhs->w_fr) {
    return false;
  }
  // w_rl
  if (lhs->w_rl != rhs->w_rl) {
    return false;
  }
  // w_rr
  if (lhs->w_rr != rhs->w_rr) {
    return false;
  }
  // s
  if (lhs->s != rhs->s) {
    return false;
  }
  return true;
}

bool
vd_msgs__msg__VDstate__copy(
  const vd_msgs__msg__VDstate * input,
  vd_msgs__msg__VDstate * output)
{
  if (!input || !output) {
    return false;
  }
  // vx
  output->vx = input->vx;
  // vy
  output->vy = input->vy;
  // r
  output->r = input->r;
  // x
  output->x = input->x;
  // y
  output->y = input->y;
  // psi
  output->psi = input->psi;
  // w_fl
  output->w_fl = input->w_fl;
  // w_fr
  output->w_fr = input->w_fr;
  // w_rl
  output->w_rl = input->w_rl;
  // w_rr
  output->w_rr = input->w_rr;
  // s
  output->s = input->s;
  return true;
}

vd_msgs__msg__VDstate *
vd_msgs__msg__VDstate__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vd_msgs__msg__VDstate * msg = (vd_msgs__msg__VDstate *)allocator.allocate(sizeof(vd_msgs__msg__VDstate), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(vd_msgs__msg__VDstate));
  bool success = vd_msgs__msg__VDstate__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
vd_msgs__msg__VDstate__destroy(vd_msgs__msg__VDstate * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    vd_msgs__msg__VDstate__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
vd_msgs__msg__VDstate__Sequence__init(vd_msgs__msg__VDstate__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vd_msgs__msg__VDstate * data = NULL;

  if (size) {
    data = (vd_msgs__msg__VDstate *)allocator.zero_allocate(size, sizeof(vd_msgs__msg__VDstate), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = vd_msgs__msg__VDstate__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        vd_msgs__msg__VDstate__fini(&data[i - 1]);
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
vd_msgs__msg__VDstate__Sequence__fini(vd_msgs__msg__VDstate__Sequence * array)
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
      vd_msgs__msg__VDstate__fini(&array->data[i]);
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

vd_msgs__msg__VDstate__Sequence *
vd_msgs__msg__VDstate__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vd_msgs__msg__VDstate__Sequence * array = (vd_msgs__msg__VDstate__Sequence *)allocator.allocate(sizeof(vd_msgs__msg__VDstate__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = vd_msgs__msg__VDstate__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
vd_msgs__msg__VDstate__Sequence__destroy(vd_msgs__msg__VDstate__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    vd_msgs__msg__VDstate__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
vd_msgs__msg__VDstate__Sequence__are_equal(const vd_msgs__msg__VDstate__Sequence * lhs, const vd_msgs__msg__VDstate__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!vd_msgs__msg__VDstate__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
vd_msgs__msg__VDstate__Sequence__copy(
  const vd_msgs__msg__VDstate__Sequence * input,
  vd_msgs__msg__VDstate__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(vd_msgs__msg__VDstate);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    vd_msgs__msg__VDstate * data =
      (vd_msgs__msg__VDstate *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!vd_msgs__msg__VDstate__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          vd_msgs__msg__VDstate__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!vd_msgs__msg__VDstate__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
