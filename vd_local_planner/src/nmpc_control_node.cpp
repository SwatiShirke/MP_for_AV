#include <vd_local_planner/nmpc_control.h>
#include <rclcpp/rclcpp.hpp>
#include <rclcpp_components/register_node_macro.hpp>
#include <geometry_msgs/msg/point_stamped.hpp>
#include <geometry_msgs/msg/pose_stamped.hpp>
#include <nav_msgs/msg/odometry.hpp>
#include <nav_msgs/msg/path.hpp>
#include <sensor_msgs/msg/imu.hpp>
#include <std_msgs/msg/bool.hpp>
#include <std_msgs/msg/empty.hpp>
#include "vd_msgs/msg/vd_control_cmd.hpp"
#include "vd_msgs/msg/v_dpose.hpp"
#include "vd_msgs/msg/v_dtraj.hpp"
#include "vd_msgs/msg/v_dstate.hpp"
#include "carla_msgs/msg/carla_ego_vehicle_control.hpp"


//#include "utils.hpp"
namespace nmpc_control_nodelet
{

  class NMPCControlNodelet : public rclcpp::Node
  {
  public:
    NMPCControlNodelet(const rclcpp::NodeOptions &options)
    : Node("nmpc_control_nodelet", options),
    frame_id_("simulator"),
    set_pre_odom_quat_(false)
    {
    

    clock_ = rclcpp::Clock();
    pre_odom_quat_ << 1.0, 0.0, 0.0, 0.0;
    //std::cout << "debug breakpont 2";
    //set qos
    auto qos_profile_ = this->create_custom_qos();
    //punlsihers
    pub_control_cmd_ = this->create_publisher<carla_msgs::msg::CarlaEgoVehicleControl>("/carla/ego_vehicle/vehicle_control_cmd",qos_profile_);
    pub_ref_traj_ = this->create_publisher<nav_msgs::msg::Path>("reference_path", 1);
    pub_pred_traj_ = this->create_publisher<nav_msgs::msg::Path>("predicted_path", 1);   
    pub_vd_cmd_ = this->create_publisher<vd_msgs::msg::VDControlCMD>("mpc_cmd", qos_profile_);

    //subscribers    
    sub_traj_cmd_ = this->create_subscription<nav_msgs::msg::Path>(
      "/carla/ego_vehicle/waypoints", qos_profile_, std::bind(&NMPCControlNodelet::referenceCallback, this, std::placeholders::_1));
    sub_odometry_ = this->create_subscription<nav_msgs::msg::Odometry>(
      "/carla/ego_vehicle/odometry", qos_profile_, std::bind(&NMPCControlNodelet::odomCallback, this, std::placeholders::_1));
    // sub_pid_cmd_ = this->create_subscription<vd_msgs::msg::VDControlCMD>(
    //   "pid_control_cmd", qos_profile_, std::bind(&NMPCControlNodelet::pidCallback, this, std::placeholders::_1));
    
    }

    EIGEN_MAKE_ALIGNED_OPERATOR_NEW
  
  private:
    NMPCControl controller_;
    rclcpp::Clock clock_;
    double mass_ = 0.278;
    double gravity_ = 9.81;
    double hover_thrust_ = mass_ * gravity_;
    float accel_cmd;
    float ref_vel;
    //double Eigen::Matrix<double, 3, 3> inertia_matrix_
    Eigen::Matrix<double, 3,3> mass_matrix_ = mass_ * Eigen::MatrixXd::Identity(3,3);
     
    // from odom callback
    std::string frame_id_;
    Eigen::Vector4d pre_odom_quat_;
    bool set_pre_odom_quat_;
    Eigen::Matrix<double,kStateSize, 1> vd_current_state; 

    // ros functions
    Eigen::Matrix<double,kStateSize, 1> get_vd_current_state();
    void publishControl();
    void publishReference();
    void publishPrediction();
    void referenceCallback(const nav_msgs::msg::Path::SharedPtr reference_msg);
    void odomCallback(const nav_msgs::msg::Odometry::SharedPtr odom_msg);
    //void pidCallback(const vd_msgs::msg::VDControlCMD::SharedPtr vd_msg);

    rclcpp::QoS create_custom_qos();
    rclcpp::Publisher<carla_msgs::msg::CarlaEgoVehicleControl>::SharedPtr pub_control_cmd_;
    rclcpp::Publisher<nav_msgs::msg::Path>::SharedPtr pub_ref_traj_;
    rclcpp::Publisher<nav_msgs::msg::Path>::SharedPtr pub_pred_traj_;       
    rclcpp::Publisher<vd_msgs::msg::VDControlCMD>::SharedPtr pub_vd_cmd_;


    rclcpp::Subscription<nav_msgs::msg::Path>::SharedPtr sub_traj_cmd_;
    rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr sub_odometry_;
    rclcpp::Subscription<vd_msgs::msg::VDControlCMD>::SharedPtr sub_pid_cmd_;
    
 };


//class functions
Eigen::Matrix<double,kStateSize, 1> NMPCControlNodelet::get_vd_current_state()
{
  return this->vd_current_state;
}

rclcpp::QoS NMPCControlNodelet::create_custom_qos() {
            // Use the correct type for the history policy
            auto history_policy = RMW_QOS_POLICY_HISTORY_KEEP_LAST;
            size_t depth = 1;

            // Create QoSInitialization with the correct arguments
            rclcpp::QoSInitialization qos_init(history_policy, depth);

            // Create QoS profile and set additional parameters
            rclcpp::QoS qos_profile(qos_init);
            qos_profile.reliability(rclcpp::ReliabilityPolicy::BestEffort);
            qos_profile.durability(rclcpp::DurabilityPolicy::Volatile);

            return qos_profile;
    }

void NMPCControlNodelet::referenceCallback(const nav_msgs::msg::Path::SharedPtr reference_msg )
{ 
  nav_msgs::msg::Path::SharedPtr filt_reference_msg(reference_msg);
  
  //initialize ref state and input variables
  Eigen::Matrix<double,kStateSize, kSamples> reference_states;
  Eigen::Matrix<double, kInputSize, kSamples> reference_inputs;
  reference_states = Eigen::Matrix<double,kStateSize, kSamples>::Zero();
  reference_inputs = Eigen::Matrix<double,kInputSize, kSamples>::Zero();
  
  this->ref_vel = filt_reference_msg->poses[0].pose.orientation.w;
  if (filt_reference_msg->poses.size() > 1)
  {
    auto iterator(filt_reference_msg->poses.begin());
    for (int i=0; i < kSamples; i++)
    { 
      //std::cout <<iterator->pose.position.x << " " << iterator->pose.position.y << std::endl;
       
      reference_states.col(i) << iterator->pose.position.x,
                                  iterator->pose.position.y, 
                                  iterator->pose.orientation.x,
                                  iterator->pose.orientation.w;
                                  
                                 
    
      reference_inputs.col(i) << 0, 0, 0;
      iterator++;
    }
  }
  else if(filt_reference_msg->poses.size() == 1)
  { 

    reference_states = (Eigen::Matrix<double, kStateSize, 1>() << filt_reference_msg->poses[0].pose.position.x,
                                                                  filt_reference_msg->poses[0].pose.position.y,
                                                                  filt_reference_msg->poses[0].pose.orientation.x,
                                                                  filt_reference_msg->poses[0].pose.orientation.w).finished().replicate(1, kSamples);
    
    
    reference_inputs = (Eigen::Matrix<double, kInputSize, 1>() << 0,0,0).finished().replicate(1, kSamples);
        
    }
  
  else 
  {
    Eigen::Matrix<double, kStateSize, 1> state = this->get_vd_current_state();
    for (int i=0; i < kSamples; i++)
    {       
      reference_states.col(i) = state;
      //std::cout << "x :" <<state(0) << "y :" << state(1) << "z :" << state(2)<< '\n'; 
      reference_inputs.col(i) << 0,0,0;
    }
  }


  controller_.setReferenceStates(reference_states);
  controller_.setReferenceInputs(reference_inputs);

  
  // run controller at reference frequency
  //std::cout <<"running mpc controller now"<< '\n';  
  controller_.run();

  // publish control and predicted path
  publishControl();
  //publishReference();
  publishPrediction();
}

void NMPCControlNodelet::odomCallback(const nav_msgs::msg::Odometry::SharedPtr odom_msg)
{
  Eigen::Matrix<double, kStateSize, 1> state;
  //frame_id_ = odom_msg->header.frame_id;
  state(0) = odom_msg->pose.pose.position.x;
  state(1) = odom_msg->pose.pose.position.y;
  state(2) = odom_msg->pose.pose.orientation.x;
  state(3) = odom_msg->twist.twist.linear.x;
 
  
  this->vd_current_state = state;
  controller_.setState(state);
}
 

// void NMPCControlNodelet::pidCallback(const vd_msgs::msg::VDControlCMD::SharedPtr vd_msg)
// {
//   this->accel_cmd = vd_msg->acceleration;
  
// }
 

void NMPCControlNodelet::publishControl()
{ 
  //std::cout << "here inside control" << std::endl;
  Eigen::Matrix<double, kInputSize, 1> pred_input = controller_.getPredictedInput();
  //carla_msgs::msg::CarlaEgoVehicleControl vd_control_msg;
  //vd_control_msg.header.stamp = clock_.now();
  
  // if (this->accel_cmd >= 0)
  // {
  //   vd_control_msg.throttle = this->accel_cmd /8.5 ;
  //   vd_control_msg.steer = (pred_input(1) + pred_input(2))/ (2 * 0.7) ; //40 degree steering angle 
  //   vd_control_msg.brake = 0;
  // }
  // else
  // {
  //   vd_control_msg.throttle = 0;
  //   vd_control_msg.steer = (pred_input(1) + pred_input(2))/(2 * 0.7);
  //   vd_control_msg.brake = -1 * this->accel_cmd / 8.5;
  // }
  //std::cout<< "pred_input" << pred_input << '\n';
  // int lf = 2.56/2;
  // int lr = 2.56/2;
  // float beta = atan2(lr , (lf + lr) * tan(vd_control_msg.steer));

  //std::cout << "beta" << beta << std::endl;
  //pub_control_cmd_->publish(vd_control_msg);

  vd_msgs::msg::VDControlCMD vd_control_msg;
  vd_control_msg.velocity = this->ref_vel;
  vd_control_msg.acceleration = pred_input(0);  
  vd_control_msg.steering_angle = (pred_input(1) + pred_input(2))/(2 * 0.7);
  pub_vd_cmd_->publish(vd_control_msg); 
}

void NMPCControlNodelet::publishReference()
{
  Eigen::Matrix<double, kStateSize, kSamples> reference_states = controller_.getReferenceStates();  
  nav_msgs::msg::Path path_msg;
  path_msg.header.stamp = clock_.now();
  path_msg.header.frame_id = frame_id_;
  geometry_msgs::msg::PoseStamped pose;
  for (int i=0; i < kSamples; i++)
  { 
    pose.header.stamp = clock_.now();
    pose.header.frame_id = frame_id_;
    pose.pose.position.x = reference_states(0,i);
    pose.pose.position.y = reference_states(1, i);
    pose.pose.position.z = 0;

    pose.pose.orientation.w = 1;
    pose.pose.orientation.x = 0;
    pose.pose.orientation.y = 0;
    pose.pose.orientation.z = 0;
    path_msg.poses.push_back(pose);    
  }

  pub_ref_traj_->publish(path_msg);
}

void NMPCControlNodelet::publishPrediction()
{
  Eigen::Matrix<double, kStateSize, kSamples> reference_states = controller_.getPredictedStates();
  nav_msgs::msg::Path path_msg;
  path_msg.header.stamp = clock_.now();
  path_msg.header.frame_id = frame_id_;
  geometry_msgs::msg::PoseStamped pose;
  //std::cout << "starting here" << std::endl;
  for (int i=0; i < kSamples; i++)
  { 
    //std::cout << " pred x " << reference_states(0,i) << " pred_y " << reference_states(1,i) << " pred_yaw " << reference_states(2,i) << " pred_vel " << reference_states(3,i) << '\n';
    pose.header.stamp = clock_.now();
    pose.header.frame_id = frame_id_;
    pose.pose.position.x = reference_states(0,i);
    pose.pose.position.y = reference_states(1, i);
    pose.pose.position.z = 0;
    pose.pose.orientation.w = 1;
    pose.pose.orientation.x = 0;
    pose.pose.orientation.y = 0;
    pose.pose.orientation.z = 0;
    path_msg.poses.push_back(pose);    
  }

  pub_pred_traj_->publish(path_msg);
}


}// namespace nodelet ends here

//RCLCPP_COMPONENTS_REGISTER_NODE(nmpc_control_nodelet::NMPCControlNodelet)

int main(int argc, char *argv[])
{ 
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<nmpc_control_nodelet::NMPCControlNodelet>(rclcpp::NodeOptions())); 
  rclcpp::shutdown();
  return 0;
}