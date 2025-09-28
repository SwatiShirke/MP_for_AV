# generated from rosidl_generator_py/resource/_idl.py.em
# with input from vd_msgs:msg/VDpose.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_VDpose(type):
    """Metaclass of message 'VDpose'."""

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
                'vd_msgs.msg.VDpose')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__v_dpose
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__v_dpose
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__v_dpose
            cls._TYPE_SUPPORT = module.type_support_msg__msg__v_dpose
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__v_dpose

            from std_msgs.msg import Header
            if Header.__class__._TYPE_SUPPORT is None:
                Header.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class VDpose(metaclass=Metaclass_VDpose):
    """Message class 'VDpose'."""

    __slots__ = [
        '_header',
        '_x',
        '_y',
        '_psi',
        '_velocity',
        '_distance',
        '_x_lane_center',
        '_y_lane_center',
        '_yaw_lane_center',
        '_total_distance',
        '_acceleration',
        '_steering_angle',
        '_length',
        '_width',
    ]

    _fields_and_field_types = {
        'header': 'std_msgs/Header',
        'x': 'double',
        'y': 'double',
        'psi': 'double',
        'velocity': 'double',
        'distance': 'double',
        'x_lane_center': 'double',
        'y_lane_center': 'double',
        'yaw_lane_center': 'double',
        'total_distance': 'double',
        'acceleration': 'double',
        'steering_angle': 'double',
        'length': 'double',
        'width': 'double',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'Header'),  # noqa: E501
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
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from std_msgs.msg import Header
        self.header = kwargs.get('header', Header())
        self.x = kwargs.get('x', float())
        self.y = kwargs.get('y', float())
        self.psi = kwargs.get('psi', float())
        self.velocity = kwargs.get('velocity', float())
        self.distance = kwargs.get('distance', float())
        self.x_lane_center = kwargs.get('x_lane_center', float())
        self.y_lane_center = kwargs.get('y_lane_center', float())
        self.yaw_lane_center = kwargs.get('yaw_lane_center', float())
        self.total_distance = kwargs.get('total_distance', float())
        self.acceleration = kwargs.get('acceleration', float())
        self.steering_angle = kwargs.get('steering_angle', float())
        self.length = kwargs.get('length', float())
        self.width = kwargs.get('width', float())

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
        if self.header != other.header:
            return False
        if self.x != other.x:
            return False
        if self.y != other.y:
            return False
        if self.psi != other.psi:
            return False
        if self.velocity != other.velocity:
            return False
        if self.distance != other.distance:
            return False
        if self.x_lane_center != other.x_lane_center:
            return False
        if self.y_lane_center != other.y_lane_center:
            return False
        if self.yaw_lane_center != other.yaw_lane_center:
            return False
        if self.total_distance != other.total_distance:
            return False
        if self.acceleration != other.acceleration:
            return False
        if self.steering_angle != other.steering_angle:
            return False
        if self.length != other.length:
            return False
        if self.width != other.width:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def header(self):
        """Message field 'header'."""
        return self._header

    @header.setter
    def header(self, value):
        if __debug__:
            from std_msgs.msg import Header
            assert \
                isinstance(value, Header), \
                "The 'header' field must be a sub message of type 'Header'"
        self._header = value

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
    def velocity(self):
        """Message field 'velocity'."""
        return self._velocity

    @velocity.setter
    def velocity(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'velocity' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'velocity' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._velocity = value

    @builtins.property
    def distance(self):
        """Message field 'distance'."""
        return self._distance

    @distance.setter
    def distance(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'distance' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'distance' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._distance = value

    @builtins.property
    def x_lane_center(self):
        """Message field 'x_lane_center'."""
        return self._x_lane_center

    @x_lane_center.setter
    def x_lane_center(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'x_lane_center' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'x_lane_center' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._x_lane_center = value

    @builtins.property
    def y_lane_center(self):
        """Message field 'y_lane_center'."""
        return self._y_lane_center

    @y_lane_center.setter
    def y_lane_center(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'y_lane_center' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'y_lane_center' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._y_lane_center = value

    @builtins.property
    def yaw_lane_center(self):
        """Message field 'yaw_lane_center'."""
        return self._yaw_lane_center

    @yaw_lane_center.setter
    def yaw_lane_center(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'yaw_lane_center' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'yaw_lane_center' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._yaw_lane_center = value

    @builtins.property
    def total_distance(self):
        """Message field 'total_distance'."""
        return self._total_distance

    @total_distance.setter
    def total_distance(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'total_distance' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'total_distance' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._total_distance = value

    @builtins.property
    def acceleration(self):
        """Message field 'acceleration'."""
        return self._acceleration

    @acceleration.setter
    def acceleration(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'acceleration' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'acceleration' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._acceleration = value

    @builtins.property
    def steering_angle(self):
        """Message field 'steering_angle'."""
        return self._steering_angle

    @steering_angle.setter
    def steering_angle(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'steering_angle' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'steering_angle' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._steering_angle = value

    @builtins.property
    def length(self):
        """Message field 'length'."""
        return self._length

    @length.setter
    def length(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'length' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'length' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._length = value

    @builtins.property
    def width(self):
        """Message field 'width'."""
        return self._width

    @width.setter
    def width(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'width' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'width' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._width = value
