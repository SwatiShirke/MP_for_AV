// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from vd_msgs:msg/VDstate.idl
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
#include "vd_msgs/msg/detail/v_dstate__struct.h"
#include "vd_msgs/msg/detail/v_dstate__functions.h"


ROSIDL_GENERATOR_C_EXPORT
bool vd_msgs__msg__v_dstate__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[30];
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
    assert(strncmp("vd_msgs.msg._v_dstate.VDstate", full_classname_dest, 29) == 0);
  }
  vd_msgs__msg__VDstate * ros_message = _ros_message;
  {  // vx
    PyObject * field = PyObject_GetAttrString(_pymsg, "vx");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->vx = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // vy
    PyObject * field = PyObject_GetAttrString(_pymsg, "vy");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->vy = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // r
    PyObject * field = PyObject_GetAttrString(_pymsg, "r");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->r = PyFloat_AS_DOUBLE(field);
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
  {  // w_fl
    PyObject * field = PyObject_GetAttrString(_pymsg, "w_fl");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->w_fl = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // w_fr
    PyObject * field = PyObject_GetAttrString(_pymsg, "w_fr");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->w_fr = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // w_rl
    PyObject * field = PyObject_GetAttrString(_pymsg, "w_rl");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->w_rl = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // w_rr
    PyObject * field = PyObject_GetAttrString(_pymsg, "w_rr");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->w_rr = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // s
    PyObject * field = PyObject_GetAttrString(_pymsg, "s");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->s = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * vd_msgs__msg__v_dstate__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of VDstate */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("vd_msgs.msg._v_dstate");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "VDstate");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  vd_msgs__msg__VDstate * ros_message = (vd_msgs__msg__VDstate *)raw_ros_message;
  {  // vx
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->vx);
    {
      int rc = PyObject_SetAttrString(_pymessage, "vx", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // vy
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->vy);
    {
      int rc = PyObject_SetAttrString(_pymessage, "vy", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // r
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->r);
    {
      int rc = PyObject_SetAttrString(_pymessage, "r", field);
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
  {  // w_fl
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->w_fl);
    {
      int rc = PyObject_SetAttrString(_pymessage, "w_fl", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // w_fr
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->w_fr);
    {
      int rc = PyObject_SetAttrString(_pymessage, "w_fr", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // w_rl
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->w_rl);
    {
      int rc = PyObject_SetAttrString(_pymessage, "w_rl", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // w_rr
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->w_rr);
    {
      int rc = PyObject_SetAttrString(_pymessage, "w_rr", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // s
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->s);
    {
      int rc = PyObject_SetAttrString(_pymessage, "s", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
