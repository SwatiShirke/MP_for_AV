// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from vd_msgs:msg/VDList.idl
// generated code does not contain a copyright notice

#ifndef VD_MSGS__MSG__DETAIL__VD_LIST__FUNCTIONS_H_
#define VD_MSGS__MSG__DETAIL__VD_LIST__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "vd_msgs/msg/rosidl_generator_c__visibility_control.h"

#include "vd_msgs/msg/detail/vd_list__struct.h"

/// Initialize msg/VDList message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * vd_msgs__msg__VDList
 * )) before or use
 * vd_msgs__msg__VDList__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_vd_msgs
bool
vd_msgs__msg__VDList__init(vd_msgs__msg__VDList * msg);

/// Finalize msg/VDList message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_vd_msgs
void
vd_msgs__msg__VDList__fini(vd_msgs__msg__VDList * msg);

/// Create msg/VDList message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * vd_msgs__msg__VDList__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_vd_msgs
vd_msgs__msg__VDList *
vd_msgs__msg__VDList__create();

/// Destroy msg/VDList message.
/**
 * It calls
 * vd_msgs__msg__VDList__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_vd_msgs
void
vd_msgs__msg__VDList__destroy(vd_msgs__msg__VDList * msg);

/// Check for msg/VDList message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_vd_msgs
bool
vd_msgs__msg__VDList__are_equal(const vd_msgs__msg__VDList * lhs, const vd_msgs__msg__VDList * rhs);

/// Copy a msg/VDList message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_vd_msgs
bool
vd_msgs__msg__VDList__copy(
  const vd_msgs__msg__VDList * input,
  vd_msgs__msg__VDList * output);

/// Initialize array of msg/VDList messages.
/**
 * It allocates the memory for the number of elements and calls
 * vd_msgs__msg__VDList__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_vd_msgs
bool
vd_msgs__msg__VDList__Sequence__init(vd_msgs__msg__VDList__Sequence * array, size_t size);

/// Finalize array of msg/VDList messages.
/**
 * It calls
 * vd_msgs__msg__VDList__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_vd_msgs
void
vd_msgs__msg__VDList__Sequence__fini(vd_msgs__msg__VDList__Sequence * array);

/// Create array of msg/VDList messages.
/**
 * It allocates the memory for the array and calls
 * vd_msgs__msg__VDList__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_vd_msgs
vd_msgs__msg__VDList__Sequence *
vd_msgs__msg__VDList__Sequence__create(size_t size);

/// Destroy array of msg/VDList messages.
/**
 * It calls
 * vd_msgs__msg__VDList__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_vd_msgs
void
vd_msgs__msg__VDList__Sequence__destroy(vd_msgs__msg__VDList__Sequence * array);

/// Check for msg/VDList message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_vd_msgs
bool
vd_msgs__msg__VDList__Sequence__are_equal(const vd_msgs__msg__VDList__Sequence * lhs, const vd_msgs__msg__VDList__Sequence * rhs);

/// Copy an array of msg/VDList messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_vd_msgs
bool
vd_msgs__msg__VDList__Sequence__copy(
  const vd_msgs__msg__VDList__Sequence * input,
  vd_msgs__msg__VDList__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // VD_MSGS__MSG__DETAIL__VD_LIST__FUNCTIONS_H_
