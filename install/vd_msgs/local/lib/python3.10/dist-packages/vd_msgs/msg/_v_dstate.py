# generated from rosidl_generator_py/resource/_idl.py.em
# with input from vd_msgs:msg/VDstate.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_VDstate(type):
    """Metaclass of message 'VDstate'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('vd_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'vd_msgs.msg.VDstate')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__v_dstate
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__v_dstate
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__v_dstate
            cls._TYPE_SUPPORT = module.type_support_msg__msg__v_dstate
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__v_dstate

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class VDstate(metaclass=Metaclass_VDstate):
    """Message class 'VDstate'."""

    __slots__ = [
        '_vx',
        '_vy',
        '_r',
        '_x',
        '_y',
        '_psi',
        '_w_fl',
        '_w_fr',
        '_w_rl',
        '_w_rr',
        '_s',
    ]

    _fields_and_field_types = {
        'vx': 'double',
        'vy': 'double',
        'r': 'double',
        'x': 'double',
        'y': 'double',
        'psi': 'double',
        'w_fl': 'double',
        'w_fr': 'double',
        'w_rl': 'double',
        'w_rr': 'double',
        's': 'double',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.vx = kwargs.get('vx', float())
        self.vy = kwargs.get('vy', float())
        self.r = kwargs.get('r', float())
        self.x = kwargs.get('x', float())
        self.y = kwargs.get('y', float())
        self.psi = kwargs.get('psi', float())
        self.w_fl = kwargs.get('w_fl', float())
        self.w_fr = kwargs.get('w_fr', float())
        self.w_rl = kwargs.get('w_rl', float())
        self.w_rr = kwargs.get('w_rr', float())
        self.s = kwargs.get('s', float())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.vx != other.vx:
            return False
        if self.vy != other.vy:
            return False
        if self.r != other.r:
            return False
        if self.x != other.x:
            return False
        if self.y != other.y:
            return False
        if self.psi != other.psi:
            return False
        if self.w_fl != other.w_fl:
            return False
        if self.w_fr != other.w_fr:
            return False
        if self.w_rl != other.w_rl:
            return False
        if self.w_rr != other.w_rr:
            return False
        if self.s != other.s:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def vx(self):
        """Message field 'vx'."""
        return self._vx

    @vx.setter
    def vx(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'vx' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'vx' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._vx = value

    @builtins.property
    def vy(self):
        """Message field 'vy'."""
        return self._vy

    @vy.setter
    def vy(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'vy' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'vy' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._vy = value

    @builtins.property
    def r(self):
        """Message field 'r'."""
        return self._r

    @r.setter
    def r(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'r' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'r' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._r = value

    @builtins.property
    def x(self):
        """Message field 'x'."""
        return self._x

    @x.setter
    def x(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'x' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'x' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._x = value

    @builtins.property
    def y(self):
        """Message field 'y'."""
        return self._y

    @y.setter
    def y(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'y' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'y' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._y = value

    @builtins.property
    def psi(self):
        """Message field 'psi'."""
        return self._psi

    @psi.setter
    def psi(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'psi' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'psi' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._psi = value

    @builtins.property
    def w_fl(self):
        """Message field 'w_fl'."""
        return self._w_fl

    @w_fl.setter
    def w_fl(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'w_fl' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'w_fl' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._w_fl = value

    @builtins.property
    def w_fr(self):
        """Message field 'w_fr'."""
        return self._w_fr

    @w_fr.setter
    def w_fr(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'w_fr' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'w_fr' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._w_fr = value

    @builtins.property
    def w_rl(self):
        """Message field 'w_rl'."""
        return self._w_rl

    @w_rl.setter
    def w_rl(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'w_rl' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'w_rl' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._w_rl = value

    @builtins.property
    def w_rr(self):
        """Message field 'w_rr'."""
        return self._w_rr

    @w_rr.setter
    def w_rr(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'w_rr' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'w_rr' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._w_rr = value

    @builtins.property
    def s(self):
        """Message field 's'."""
        return self._s

    @s.setter
    def s(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 's' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 's' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._s = value
