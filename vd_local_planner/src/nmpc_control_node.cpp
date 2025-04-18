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
#include "vd_msgs/msg/vd_list.hpp"  

#include <casadi/casadi.hpp>
#include <vd_local_planner/polytopes.h>
#include "vd_local_planner/cbf_solver.h"
using namespace casadi;
#include <vector>
#include <cmath>

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
    
    //subscribers    
    sub_traj_cmd_ = this->create_subscription<nav_msgs::msg::Path>(
      "/carla/ego_vehicle/waypoints", qos_profile_, std::bind(&NMPCControlNodelet::referenceCallback, this, std::placeholders::_1));
    sub_odometry_ = this->create_subscription<nav_msgs::msg::Odometry>(
      "/carla/ego_vehicle/odometry", qos_profile_, std::bind(&NMPCControlNodelet::odomCallback, this, std::placeholders::_1));
    sub_vd_list_ = this->create_subscription<vd_msgs::msg::VDList>(
      "neighbour_VDs", qos_profile_, std::bind(&NMPCControlNodelet::VD_list_callback, this, std::placeholders::_1));
    
    VD_ptr =std::make_shared<VD_polytope>(L, W);    
    std::pair<Eigen::Matrix<double, m_bot, n_bot >, Eigen::Matrix<double, m_bot, 1 >>VD_poly = VD_ptr->get_matrices();   
    this->A_bot = VD_poly.first;    
    this->B_bot = VD_poly.second;  
    
    }

    EIGEN_MAKE_ALIGNED_OPERATOR_NEW
  
  private:
    NMPCControl controller_;
    rclcpp::Clock clock_;
        
    
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
    void VD_list_callback(const vd_msgs::msg::VDList::SharedPtr VD_list_msg);

    void Cal_CBF_guess(void);
    int call_solver( double& results , const Eigen::Matrix<double, m_bot, n_bot>& A_bot, const Eigen::Matrix<double, m_bot, 1> B_bot, 
      const Eigen::Matrix<double, m_obj, n_obj> A_obj, const Eigen::Matrix<double, m_obj, 1> B_obj, const Eigen::Vector4d points);    
    std::vector<std::vector<float>> vd_list; 



    rclcpp::QoS create_custom_qos();
    rclcpp::Publisher<carla_msgs::msg::CarlaEgoVehicleControl>::SharedPtr pub_control_cmd_;
    rclcpp::Publisher<nav_msgs::msg::Path>::SharedPtr pub_ref_traj_;
    rclcpp::Publisher<nav_msgs::msg::Path>::SharedPtr pub_pred_traj_; 
   
    rclcpp::Subscription<nav_msgs::msg::Path>::SharedPtr sub_traj_cmd_;
    rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr sub_odometry_;
    rclcpp::Subscription<vd_msgs::msg::VDList>::SharedPtr sub_vd_list_;

    //VD polytope
    float L = 4.56;
    float W = 2.08;
    std::shared_ptr<VD_polytope> VD_ptr;
    Eigen::Matrix<double, m_bot, n_bot > A_bot;
    Eigen::Matrix<double, m_bot, 1 > B_bot;    
    
    
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
  // float x, y, theta, lenght, width;
  //double steer_angle_in, steer_angle_out, R_curve; 
  
  if (filt_reference_msg->poses.size() > 1)
  {
    auto iterator(filt_reference_msg->poses.begin());
    for (int i=0; i < kSamples; i++)
    { 
      //std::cout << iterator->pose.position.x << std::endl;    
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
  
  Cal_CBF_guess();

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


void NMPCControlNodelet::Cal_CBF_guess(void)
{ 
  
  //vd information 
  Eigen::Vector2d vd_pos;
  Eigen::Matrix<double, n_bot, n_bot > R_bot;
  Eigen::Vector2d obj_pos;
  Eigen::Matrix<double, n_obj, n_obj > R_obj;

  float vd_theta = this->vd_current_state(2);     
  R_bot << cos(vd_theta),  -sin(vd_theta), 
           sin(vd_theta), cos(vd_theta);  
  vd_pos << vd_current_state(0), vd_current_state(1);
  
  std::cout << "A_bot" << A_bot << std::endl;
  std::cout << "B_bot" << B_bot << std::endl;
  std::cout << "vd_pos" << vd_pos << std::endl;
  std::cout << "vd_theta" << vd_theta << std::endl;
  std::cout << "R_bot" << R_bot << std::endl;


  auto A_bot_world = A_bot * R_bot.transpose(); 
  auto B_bot_world = (A_bot * R_bot.transpose()) * vd_pos + B_bot;

  //polytope info
  Eigen::Matrix<double, m_obj, n_obj> A_obj;
  Eigen::Matrix<double , m_obj, 1> B_obj;  
  Eigen::Vector4d points;                             //concatenated point 1 and 2 
  A_obj << -1, 0, 
            0, -1, 
            1, 0, 
            0, 1;                                    //normal vectors
            
  float obj_x, obj_y, obj_theta, obj_length, obj_width;                   
  double results;
  // call solver to find intial guess for CBF

  std::cout << "vd_list_size" << vd_list.size() << std::endl;

  for(auto vd_vec : vd_list)
  {  
    obj_x = vd_vec[0];
    obj_y = vd_vec[1];
    obj_theta = vd_vec[2];
    obj_length = vd_vec[3];
    obj_width = vd_vec[4];
    points << vd_pos(0),vd_pos(1) , obj_x, obj_y; 
    R_obj << cos(obj_theta),  -sin(obj_theta), 
             sin(obj_theta), cos(obj_theta);  
    obj_pos << obj_x, obj_y; 
    B_obj <<  obj_length/2, obj_width/2, obj_length/2, obj_width/2;     
    std::cout << "A_obj" << A_obj << std::endl;
    std::cout << "B_obj" << B_obj << std::endl;
    std::cout << "obj_pos" << obj_pos << std::endl;
    std::cout << "obj_theta" << obj_theta << std::endl;
    std::cout << "R_obj" << R_obj << std::endl;    
      
    //find obstacle polytope in world frame
    auto A_obj_world = A_obj * R_obj.transpose();
    auto B_obj_world =(A_obj * R_obj.transpose() * obj_pos ) + B_obj; 
    auto status = call_solver(results, A_bot_world, B_bot_world, A_obj_world, B_obj_world, points);
    std::cout << "here" << std::endl;
  } 

 }

int NMPCControlNodelet::call_solver(double& results , const Eigen::Matrix<double, m_bot, n_bot>& A_bot, const Eigen::Matrix<double, m_bot, 1> B_bot, 
  const Eigen::Matrix<double, m_obj, n_obj> A_obj, const Eigen::Matrix<double, m_obj, 1> B_obj, const Eigen::Vector4d points) 
  { 
    
    const casadi_real* arg[6];    
    casadi_real* res[6];
    casadi_real w[cbf_solver_SZ_W] = {};
    casadi_int iw[cbf_solver_SZ_IW] = {};    
   
    std::vector<double> vec;
    vec.reserve(A_bot.size()+ B_bot.size() + A_obj.size() + B_obj.size());
    vec.insert(vec.end(), A_bot.data(), A_bot.data() + A_bot.size());   
    vec.insert(vec.end(), B_bot.data(), B_bot.data() + B_bot.size());
    vec.insert(vec.end(), A_obj.data(), A_obj.data() + A_obj.size());
    vec.insert(vec.end(), B_obj.data(), B_obj.data() + B_obj.size());   
    
    Eigen::Vector4d lbx = -1 * casadi::inf * Eigen::Vector4d::Ones();
    Eigen::Vector4d ubx = casadi::inf * Eigen::Vector4d::Ones();
    Eigen::VectorXd lbg = -1 * casadi::inf * Eigen::VectorXd::Ones(8);
    Eigen::VectorXd ubg = Eigen::VectorXd::Zero(8);

        
    Eigen::Vector4d res_points;                     // refer cbf_solver.cpp file to know input output
    casadi_real cost;
    Eigen::VectorXd res_g(8);
    Eigen::Vector4d lam_x;
    Eigen::VectorXd lam_g(8);
    Eigen::VectorXd lam_p(24);
    
    arg[0] = points.data();  
    arg[1] =  vec.data(); 
    arg[2] = lbx.data();
    arg[3] = ubx.data();
    arg[4]  = lbg.data();
    arg[5]  = ubg.data();     
    res[0] = res_points.data();
    res[1] = &cost;
    res[2] = res_g.data();
    res[3] = lam_x.data();
    res[4] = lam_g.data();
    res[5] = lam_p.data();
    int status = cbf_solver(arg, res, iw, w, 0);
    results = ca.sqrt(cost);
    
    std::cout << "status" << status << std::endl;
    std::cout << "distance "<<results << std::endl;
    return status;}


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
  
void NMPCControlNodelet::publishControl()
{ 
  Eigen::Matrix<double, kInputSize, 1> pred_input = controller_.getPredictedInput();
  carla_msgs::msg::CarlaEgoVehicleControl vd_control_msg;
  vd_control_msg.header.stamp = clock_.now();
  //vd_control_ms.header.frame_id = frame_id_;  
  
  if (pred_input(0) >= 0)
  {
    vd_control_msg.throttle = 0; //pred_input(0)/8.5 ;
    vd_control_msg.steer = (pred_input(1) + pred_input(2))/ (2 * 0.7) ; //40 degree steering angle 
    vd_control_msg.brake = 0;
  }
  else
  {
    vd_control_msg.throttle = 0;
    vd_control_msg.steer = (pred_input(1) + pred_input(2))/(2 * 0.7);
    vd_control_msg.brake = 0; //-1 *(pred_input(0) ) / 8.5;
  }
  std::cout<< "pred_input" << pred_input << '\n';
  //RCLCPP_INFO(this->get_logger(), pred_input(0));
  pub_control_cmd_->publish(vd_control_msg);

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


void NMPCControlNodelet::VD_list_callback(const vd_msgs::msg::VDList::SharedPtr VD_list_msg)
{ 
  auto iterator = VD_list_msg->vdlist.begin();
  this->vd_list.clear();
  

  while (iterator != VD_list_msg->vdlist.end())
  {
    this->vd_list.push_back({iterator->x, iterator->y, iterator->yaw, iterator->length, iterator->width});
    //std::cout << iterator->x << iterator->y << iterator->yaw << iterator->length << iterator->width << std::endl;
    ++iterator;
  }
  

 

}


}// namespace nodelet ends here

//RCLCPP_COMPONENTS_REGISTER_NODE(nmpc_control_nodelet::NMPCControlNodelet)

int main(int argc, char *argv[])
{ std::cout<<"here..inside main"<<'\n';
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<nmpc_control_nodelet::NMPCControlNodelet>(rclcpp::NodeOptions())); 
  rclcpp::shutdown();
  return 0;
}