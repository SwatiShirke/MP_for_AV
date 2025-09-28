// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from vd_msgs:msg/VDpose.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "vd_msgs/msg/detail/v_dpose__struct.h"
#include "vd_msgs/msg/detail/v_dpose__functions.h"

ROSIDL_GENERATOR_C_IMPORT
bool std_msgs__msg__header__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * std_msgs__msg__header__convert_to_py(void * raw_ros_message);

ROSIDL_GENERATOR_C_EXPORT
bool vd_msgs__msg__v_dpose__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[28];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("vd_msgs.msg._v_dpose.VDpose", full_classname_dest, 27) == 0);
  }
  vd_msgs__msg__VDpose * ros_message = _ros_message;
  {  // header
    PyObject * field = PyObject_GetAttrString(_pymsg, "header");
    if (!field) {
      return false;
    }
    if (!std_msgs__msg__header__convert_from_py(field, &ros_message->header)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // x
    PyObject * field = PyObject_GetAttrString(_pymsg, "x");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->x = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // y
    PyObject * field = PyObject_GetAttrString(_pymsg, "y");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->y = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // psi
    PyObject * field = PyObject_GetAttrString(_pymsg, "psi");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->psi = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // velocity
    PyObject * field = PyObject_GetAttrString(_pymsg, "velocity");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->velocity = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // distance
    PyObject * field = PyObject_GetAttrString(_pymsg, "distance");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->distance = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // x_lane_center
    PyObject * field = PyObject_GetAttrString(_pymsg, "x_lane_center");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->x_lane_center = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // y_lane_center
    PyObject * field = PyObject_GetAttrString(_pymsg, "y_lane_center");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->y_lane_center = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // yaw_lane_center
    PyObject * field = PyObject_GetAttrString(_pymsg, "yaw_lane_center");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->yaw_lane_center = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // total_distance
    PyObject * field = PyObject_GetAttrString(_pymsg, "total_distance");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->total_distance = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // acceleration
    PyObject * field = PyObject_GetAttrString(_pymsg, "acceleration");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->acceleration = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // steering_angle
    PyObject * field = PyObject_GetAttrString(_pymsg, "steering_angle");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->steering_angle = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // length
    PyObject * field = PyObject_GetAttrString(_pymsg, "length");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->length = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // width
    PyObject * field = PyObject_GetAttrString(_pymsg, "width");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->width = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * vd_msgs__msg__v_dpose__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of VDpose */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("vd_msgs.msg._v_dpose");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "VDpose");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  vd_msgs__msg__VDpose * ros_message = (vd_msgs__msg__VDpose *)raw_ros_message;
  {  // header
    PyObject * field = NULL;
    field = std_msgs__msg__header__convert_to_py(&ros_message->header);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "header", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // x
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->x);
    {
      int rc = PyObject_SetAttrString(_pymessage, "x", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // y
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->y);
    {
      int rc = PyObject_SetAttrString(_pymessage, "y", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // psi
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->psi);
    {
      int rc = PyObject_SetAttrString(_pymessage, "psi", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // velocity
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->velocity);
    {
      int rc = PyObject_SetAttrString(_pymessage, "velocity", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // distance
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->distance);
    {
      int rc = PyObject_SetAttrString(_pymessage, "distance", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // x_lane_center
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->x_lane_center);
    {
      int rc = PyObject_SetAttrString(_pymessage, "x_lane_center", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // y_lane_center
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->y_lane_center);
    {
      int rc = PyObject_SetAttrString(_pymessage, "y_lane_center", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // yaw_lane_center
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->yaw_lane_center);
    {
      int rc = PyObject_SetAttrString(_pymessage, "yaw_lane_center", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // total_distance
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->total_distance);
    {
      int rc = PyObject_SetAttrString(_pymessage, "total_distance", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // acceleration
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->acceleration);
    {
      int rc = PyObject_SetAttrString(_pymessage, "acceleration", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // steering_angle
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->steering_angle);
    {
      int rc = PyObject_SetAttrString(_pymessage, "steering_angle", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // length
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->length);
    {
      int rc = PyObject_SetAttrString(_pymessage, "length", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // width
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->width);
    {
      int rc = PyObject_SetAttrString(_pymessage, "width", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
