// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from vd_msgs:msg/VDtraj.idl
// generated code does not contain a copyright notice

#ifndef VD_MSGS__MSG__DETAIL__V_DTRAJ__FUNCTIONS_H_
#define VD_MSGS__MSG__DETAIL__V_DTRAJ__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "vd_msgs/msg/rosidl_generator_c__visibility_control.h"

#include "vd_msgs/msg/detail/v_dtraj__struct.h"

/// Initialize msg/VDtraj message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * vd_msgs__msg__VDtraj
 * )) before or use
 * vd_msgs__msg__VDtraj__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_vd_msgs
bool
vd_msgs__msg__VDtraj__init(vd_msgs__msg__VDtraj * msg);

/// Finalize msg/VDtraj message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_vd_msgs
void
vd_msgs__msg__VDtraj__fini(vd_msgs__msg__VDtraj * msg);

/// Create msg/VDtraj message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * vd_msgs__msg__VDtraj__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_vd_msgs
vd_msgs__msg__VDtraj *
vd_msgs__msg__VDtraj__create();

/// Destroy msg/VDtraj message.
/**
 * It calls
 * vd_msgs__msg__VDtraj__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_vd_msgs
void
vd_msgs__msg__VDtraj__destroy(vd_msgs__msg__VDtraj * msg);

/// Check for msg/VDtraj message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_vd_msgs
bool
vd_msgs__msg__VDtraj__are_equal(const vd_msgs__msg__VDtraj * lhs, const vd_msgs__msg__VDtraj * rhs);

/// Copy a msg/VDtraj message.
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
vd_msgs__msg__VDtraj__copy(
  const vd_msgs__msg__VDtraj * input,
  vd_msgs__msg__VDtraj * output);

/// Initialize array of msg/VDtraj messages.
/**
 * It allocates the memory for the number of elements and calls
 * vd_msgs__msg__VDtraj__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_vd_msgs
bool
vd_msgs__msg__VDtraj__Sequence__init(vd_msgs__msg__VDtraj__Sequence * array, size_t size);

/// Finalize array of msg/VDtraj messages.
/**
 * It calls
 * vd_msgs__msg__VDtraj__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_vd_msgs
void
vd_msgs__msg__VDtraj__Sequence__fini(vd_msgs__msg__VDtraj__Sequence * array);

/// Create array of msg/VDtraj messages.
/**
 * It allocates the memory for the array and calls
 * vd_msgs__msg__VDtraj__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_vd_msgs
vd_msgs__msg__VDtraj__Sequence *
vd_msgs__msg__VDtraj__Sequence__create(size_t size);

/// Destroy array of msg/VDtraj messages.
/**
 * It calls
 * vd_msgs__msg__VDtraj__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_vd_msgs
void
vd_msgs__msg__VDtraj__Sequence__destroy(vd_msgs__msg__VDtraj__Sequence * array);

/// Check for msg/VDtraj message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_vd_msgs
bool
vd_msgs__msg__VDtraj__Sequence__are_equal(const vd_msgs__msg__VDtraj__Sequence * lhs, const vd_msgs__msg__VDtraj__Sequence * rhs);

/// Copy an array of msg/VDtraj messages.
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
vd_msgs__msg__VDtraj__Sequence__copy(
  const vd_msgs__msg__VDtraj__Sequence * input,
  vd_msgs__msg__VDtraj__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // VD_MSGS__MSG__DETAIL__V_DTRAJ__FUNCTIONS_H_
