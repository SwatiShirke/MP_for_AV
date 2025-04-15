// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from vd_msgs:srv/PlannerSrv.idl
// generated code does not contain a copyright notice
#include "vd_msgs/srv/detail/planner_srv__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

bool
vd_msgs__srv__PlannerSrv_Request__init(vd_msgs__srv__PlannerSrv_Request * msg)
{
  if (!msg) {
    return false;
  }
  // x
  // y
  return true;
}

void
vd_msgs__srv__PlannerSrv_Request__fini(vd_msgs__srv__PlannerSrv_Request * msg)
{
  if (!msg) {
    return;
  }
  // x
  // y
}

bool
vd_msgs__srv__PlannerSrv_Request__are_equal(const vd_msgs__srv__PlannerSrv_Request * lhs, const vd_msgs__srv__PlannerSrv_Request * rhs)
{
  if (!lhs || !rhs) {
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
  return true;
}

bool
vd_msgs__srv__PlannerSrv_Request__copy(
  const vd_msgs__srv__PlannerSrv_Request * input,
  vd_msgs__srv__PlannerSrv_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // x
  output->x = input->x;
  // y
  output->y = input->y;
  return true;
}

vd_msgs__srv__PlannerSrv_Request *
vd_msgs__srv__PlannerSrv_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vd_msgs__srv__PlannerSrv_Request * msg = (vd_msgs__srv__PlannerSrv_Request *)allocator.allocate(sizeof(vd_msgs__srv__PlannerSrv_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(vd_msgs__srv__PlannerSrv_Request));
  bool success = vd_msgs__srv__PlannerSrv_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
vd_msgs__srv__PlannerSrv_Request__destroy(vd_msgs__srv__PlannerSrv_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    vd_msgs__srv__PlannerSrv_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
vd_msgs__srv__PlannerSrv_Request__Sequence__init(vd_msgs__srv__PlannerSrv_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vd_msgs__srv__PlannerSrv_Request * data = NULL;

  if (size) {
    data = (vd_msgs__srv__PlannerSrv_Request *)allocator.zero_allocate(size, sizeof(vd_msgs__srv__PlannerSrv_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = vd_msgs__srv__PlannerSrv_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        vd_msgs__srv__PlannerSrv_Request__fini(&data[i - 1]);
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
vd_msgs__srv__PlannerSrv_Request__Sequence__fini(vd_msgs__srv__PlannerSrv_Request__Sequence * array)
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
      vd_msgs__srv__PlannerSrv_Request__fini(&array->data[i]);
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

vd_msgs__srv__PlannerSrv_Request__Sequence *
vd_msgs__srv__PlannerSrv_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vd_msgs__srv__PlannerSrv_Request__Sequence * array = (vd_msgs__srv__PlannerSrv_Request__Sequence *)allocator.allocate(sizeof(vd_msgs__srv__PlannerSrv_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = vd_msgs__srv__PlannerSrv_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
vd_msgs__srv__PlannerSrv_Request__Sequence__destroy(vd_msgs__srv__PlannerSrv_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    vd_msgs__srv__PlannerSrv_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
vd_msgs__srv__PlannerSrv_Request__Sequence__are_equal(const vd_msgs__srv__PlannerSrv_Request__Sequence * lhs, const vd_msgs__srv__PlannerSrv_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!vd_msgs__srv__PlannerSrv_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
vd_msgs__srv__PlannerSrv_Request__Sequence__copy(
  const vd_msgs__srv__PlannerSrv_Request__Sequence * input,
  vd_msgs__srv__PlannerSrv_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(vd_msgs__srv__PlannerSrv_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    vd_msgs__srv__PlannerSrv_Request * data =
      (vd_msgs__srv__PlannerSrv_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!vd_msgs__srv__PlannerSrv_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          vd_msgs__srv__PlannerSrv_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!vd_msgs__srv__PlannerSrv_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `message`
#include "rosidl_runtime_c/string_functions.h"

bool
vd_msgs__srv__PlannerSrv_Response__init(vd_msgs__srv__PlannerSrv_Response * msg)
{
  if (!msg) {
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__init(&msg->message)) {
    vd_msgs__srv__PlannerSrv_Response__fini(msg);
    return false;
  }
  return true;
}

void
vd_msgs__srv__PlannerSrv_Response__fini(vd_msgs__srv__PlannerSrv_Response * msg)
{
  if (!msg) {
    return;
  }
  // message
  rosidl_runtime_c__String__fini(&msg->message);
}

bool
vd_msgs__srv__PlannerSrv_Response__are_equal(const vd_msgs__srv__PlannerSrv_Response * lhs, const vd_msgs__srv__PlannerSrv_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->message), &(rhs->message)))
  {
    return false;
  }
  return true;
}

bool
vd_msgs__srv__PlannerSrv_Response__copy(
  const vd_msgs__srv__PlannerSrv_Response * input,
  vd_msgs__srv__PlannerSrv_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__copy(
      &(input->message), &(output->message)))
  {
    return false;
  }
  return true;
}

vd_msgs__srv__PlannerSrv_Response *
vd_msgs__srv__PlannerSrv_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vd_msgs__srv__PlannerSrv_Response * msg = (vd_msgs__srv__PlannerSrv_Response *)allocator.allocate(sizeof(vd_msgs__srv__PlannerSrv_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(vd_msgs__srv__PlannerSrv_Response));
  bool success = vd_msgs__srv__PlannerSrv_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
vd_msgs__srv__PlannerSrv_Response__destroy(vd_msgs__srv__PlannerSrv_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    vd_msgs__srv__PlannerSrv_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
vd_msgs__srv__PlannerSrv_Response__Sequence__init(vd_msgs__srv__PlannerSrv_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vd_msgs__srv__PlannerSrv_Response * data = NULL;

  if (size) {
    data = (vd_msgs__srv__PlannerSrv_Response *)allocator.zero_allocate(size, sizeof(vd_msgs__srv__PlannerSrv_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = vd_msgs__srv__PlannerSrv_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        vd_msgs__srv__PlannerSrv_Response__fini(&data[i - 1]);
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
vd_msgs__srv__PlannerSrv_Response__Sequence__fini(vd_msgs__srv__PlannerSrv_Response__Sequence * array)
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
      vd_msgs__srv__PlannerSrv_Response__fini(&array->data[i]);
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

vd_msgs__srv__PlannerSrv_Response__Sequence *
vd_msgs__srv__PlannerSrv_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vd_msgs__srv__PlannerSrv_Response__Sequence * array = (vd_msgs__srv__PlannerSrv_Response__Sequence *)allocator.allocate(sizeof(vd_msgs__srv__PlannerSrv_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = vd_msgs__srv__PlannerSrv_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
vd_msgs__srv__PlannerSrv_Response__Sequence__destroy(vd_msgs__srv__PlannerSrv_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    vd_msgs__srv__PlannerSrv_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
vd_msgs__srv__PlannerSrv_Response__Sequence__are_equal(const vd_msgs__srv__PlannerSrv_Response__Sequence * lhs, const vd_msgs__srv__PlannerSrv_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!vd_msgs__srv__PlannerSrv_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
vd_msgs__srv__PlannerSrv_Response__Sequence__copy(
  const vd_msgs__srv__PlannerSrv_Response__Sequence * input,
  vd_msgs__srv__PlannerSrv_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(vd_msgs__srv__PlannerSrv_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    vd_msgs__srv__PlannerSrv_Response * data =
      (vd_msgs__srv__PlannerSrv_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!vd_msgs__srv__PlannerSrv_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          vd_msgs__srv__PlannerSrv_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!vd_msgs__srv__PlannerSrv_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
