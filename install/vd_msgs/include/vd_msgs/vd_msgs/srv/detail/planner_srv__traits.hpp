// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from vd_msgs:srv/PlannerSrv.idl
// generated code does not contain a copyright notice

#ifndef VD_MSGS__SRV__DETAIL__PLANNER_SRV__TRAITS_HPP_
#define VD_MSGS__SRV__DETAIL__PLANNER_SRV__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "vd_msgs/srv/detail/planner_srv__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace vd_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const PlannerSrv_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: x
  {
    out << "x: ";
    rosidl_generator_traits::value_to_yaml(msg.x, out);
    out << ", ";
  }

  // member: y
  {
    out << "y: ";
    rosidl_generator_traits::value_to_yaml(msg.y, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const PlannerSrv_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: x
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "x: ";
    rosidl_generator_traits::value_to_yaml(msg.x, out);
    out << "\n";
  }

  // member: y
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "y: ";
    rosidl_generator_traits::value_to_yaml(msg.y, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const PlannerSrv_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace vd_msgs

namespace rosidl_generator_traits
{

[[deprecated("use vd_msgs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const vd_msgs::srv::PlannerSrv_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  vd_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use vd_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const vd_msgs::srv::PlannerSrv_Request & msg)
{
  return vd_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<vd_msgs::srv::PlannerSrv_Request>()
{
  return "vd_msgs::srv::PlannerSrv_Request";
}

template<>
inline const char * name<vd_msgs::srv::PlannerSrv_Request>()
{
  return "vd_msgs/srv/PlannerSrv_Request";
}

template<>
struct has_fixed_size<vd_msgs::srv::PlannerSrv_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<vd_msgs::srv::PlannerSrv_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<vd_msgs::srv::PlannerSrv_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace vd_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const PlannerSrv_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: message
  {
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const PlannerSrv_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const PlannerSrv_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace vd_msgs

namespace rosidl_generator_traits
{

[[deprecated("use vd_msgs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const vd_msgs::srv::PlannerSrv_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  vd_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use vd_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const vd_msgs::srv::PlannerSrv_Response & msg)
{
  return vd_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<vd_msgs::srv::PlannerSrv_Response>()
{
  return "vd_msgs::srv::PlannerSrv_Response";
}

template<>
inline const char * name<vd_msgs::srv::PlannerSrv_Response>()
{
  return "vd_msgs/srv/PlannerSrv_Response";
}

template<>
struct has_fixed_size<vd_msgs::srv::PlannerSrv_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<vd_msgs::srv::PlannerSrv_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<vd_msgs::srv::PlannerSrv_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<vd_msgs::srv::PlannerSrv>()
{
  return "vd_msgs::srv::PlannerSrv";
}

template<>
inline const char * name<vd_msgs::srv::PlannerSrv>()
{
  return "vd_msgs/srv/PlannerSrv";
}

template<>
struct has_fixed_size<vd_msgs::srv::PlannerSrv>
  : std::integral_constant<
    bool,
    has_fixed_size<vd_msgs::srv::PlannerSrv_Request>::value &&
    has_fixed_size<vd_msgs::srv::PlannerSrv_Response>::value
  >
{
};

template<>
struct has_bounded_size<vd_msgs::srv::PlannerSrv>
  : std::integral_constant<
    bool,
    has_bounded_size<vd_msgs::srv::PlannerSrv_Request>::value &&
    has_bounded_size<vd_msgs::srv::PlannerSrv_Response>::value
  >
{
};

template<>
struct is_service<vd_msgs::srv::PlannerSrv>
  : std::true_type
{
};

template<>
struct is_service_request<vd_msgs::srv::PlannerSrv_Request>
  : std::true_type
{
};

template<>
struct is_service_response<vd_msgs::srv::PlannerSrv_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // VD_MSGS__SRV__DETAIL__PLANNER_SRV__TRAITS_HPP_
