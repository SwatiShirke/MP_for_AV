#include <test_pkg/nmpc_control.h>
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
    //pub_control_cmd_ = this->create_publisher<carla_msgs::msg::CarlaEgoVehicleControl>("/carla/ego_vehicle/vehicle_control_cmd",qos_profile_);
    pub_ref_traj_ = this->create_publisher<nav_msgs::msg::Path>("reference_path", 1);
    pub_pred_traj_ = this->create_publisher<vd_msgs::msg::VDtraj>("predicted_path", 1);   
    pub_vd_cmd_ = this->create_publisher<vd_msgs::msg::VDControlCMD>("mpc_cmd", qos_profile_);

    
    //subscribers    
    sub_traj_cmd_ = this->create_subscription<vd_msgs::msg::VDtraj>(
      "/carla/ego_vehicle/waypoints", qos_profile_, std::bind(&NMPCControlNodelet::referenceCallback, this, std::placeholders::_1));
    sub_vd_list_ = this->create_subscription<vd_msgs::msg::VDList>(
        "neighbour_VDs", qos_profile_, std::bind(&NMPCControlNodelet::VD_list_callback, this, std::placeholders::_1));


    if (this->is_odom_state_estimate == true)
    {  
      sub_odometry_ = this->create_subscription<vd_msgs::msg::VDpose>(
      "/vehicle_est_pose", qos_profile_, std::bind(&NMPCControlNodelet::odomCallback, this, std::placeholders::_1));    
      
    }
    else{
      sub_odometry_ = this->create_subscription<vd_msgs::msg::VDpose>(
        "/carla/ego_vehicle/odometry", qos_profile_, std::bind(&NMPCControlNodelet::odomCallback, this, std::placeholders::_1));
    }
    }

    EIGEN_MAKE_ALIGNED_OPERATOR_NEW
  
  private:
    bool is_odom_state_estimate = false;
    NMPCControl controller_;
    rclcpp::Clock clock_;
    double mass_ = 0.278;
    double gravity_ = 9.81;
    double hover_thrust_ = mass_ * gravity_;
    float accel_cmd;
    float ref_vel;
    //double init_time;     //time at the start of optimization
    rclcpp::Time init_time;
    float Tf = 5.00;     // time frame for horizon 
    
    
    static constexpr int NO_OBJECTS = 5;    
    static constexpr int PARAM_WINDOW =  6;                        // for each object, we have 6 params to set for mpc after optimization    
    static constexpr int INPUT_OFFSET = 0;
    std::vector<std::vector<float>> vd_list;

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
    void referenceCallback(const vd_msgs::msg::VDtraj::SharedPtr reference_msg);
    void odomCallback(const vd_msgs::msg::VDpose::SharedPtr odom_msg);    
    void VD_list_callback(const vd_msgs::msg::VDList::SharedPtr VD_list_msg);
    void set_ref_params(Eigen::Matrix<double, kCBF_params, kSamples> &reference_params);
    //void pidCallback(const vd_msgs::msg::VDControlCMD::SharedPtr vd_msg);

    rclcpp::QoS create_custom_qos();
    //rclcpp::Publisher<carla_msgs::msg::CarlaEgoVehicleControl>::SharedPtr pub_control_cmd_;
    rclcpp::Publisher<nav_msgs::msg::Path>::SharedPtr pub_ref_traj_;
    rclcpp::Publisher<vd_msgs::msg::VDtraj>::SharedPtr pub_pred_traj_;       
    rclcpp::Publisher<vd_msgs::msg::VDControlCMD>::SharedPtr pub_vd_cmd_;


    rclcpp::Subscription<vd_msgs::msg::VDtraj>::SharedPtr sub_traj_cmd_;
    rclcpp::Subscription<vd_msgs::msg::VDpose>::SharedPtr sub_odometry_;    
    rclcpp::Subscription<vd_msgs::msg::VDControlCMD>::SharedPtr sub_pid_cmd_;
    rclcpp::Subscription<vd_msgs::msg::VDList>::SharedPtr sub_vd_list_;
    
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


void NMPCControlNodelet::referenceCallback(const vd_msgs::msg::VDtraj::SharedPtr reference_msg )
{ 
  double total_time;
  rclcpp::Time start_time;
  rclcpp::Time end_time;

  start_time = this->get_clock()->now();
  

  vd_msgs::msg::VDtraj::SharedPtr filt_reference_msg(reference_msg);
  
  //initialize ref state and input variables
  Eigen::Matrix<double,kStateSize, kSamples> reference_states;
  Eigen::Matrix<double, kInputSize, kSamples> reference_inputs;
  Eigen::Matrix<double, kCBF_params, kSamples> reference_params;
  
  reference_states = Eigen::Matrix<double,kStateSize, kSamples>::Zero();
  reference_inputs = Eigen::Matrix<double,kInputSize, kSamples>::Zero();
  reference_params = Eigen::Matrix<double,kCBF_params, kSamples>::Zero() * 0.01;
  
  this->ref_vel = filt_reference_msg->poses[0].velocity;
  auto iterator(filt_reference_msg->poses.begin());

  // std::cout << "  " << std::endl;
  // std::cout << "vd current state" << this->vd_current_state << std::endl;
  
  if (filt_reference_msg->poses.size() > 1)
  { 
    
    for (int i=0; i < kSamples; i++)
    { 
      //std::cout << "ref recived x, y psi, vel " <<iterator->x << " " << iterator->y << " " << iterator->psi << " " << iterator->velocity <<std::endl;
       
      reference_states.col(i) << iterator->x,
                                  iterator->y, 
                                  iterator->psi,
                                  iterator->velocity,
                                  iterator->distance;

    
      reference_inputs.col(i) << 0, 0, 0;
                                 
     
      iterator++;
    }

    //reference_params.block(3, 0, 30, kSamples).setZero();

  }
  else if(filt_reference_msg->poses.size() == 1)
  { 
    //std::cout << "Here ..";    
    //std::cout <<iterator->x << " " << iterator->y << " " << iterator->psi << " " <<iterator->velocity << iterator->distance <<std::endl;

    this->ref_vel = filt_reference_msg->poses[0].velocity;
    reference_states = (Eigen::Matrix<double, kStateSize, 1>() << filt_reference_msg->poses[0].x,
                                                                  filt_reference_msg->poses[0].y,
                                                                  filt_reference_msg->poses[0].psi,
                                                                  filt_reference_msg->poses[0].velocity,
                                                                  filt_reference_msg->poses[0].distance).finished().replicate(1, kSamples);
    
    
    reference_inputs = (Eigen::Matrix<double, kInputSize, 1>() << 0,0,0).finished().replicate(1, kSamples);
     
  }
  
  else 
  { 
    //std::cout << "here in ref callback" << std::endl;
    Eigen::Matrix<double, kStateSize, 1> state = this->get_vd_current_state();
    for (int i=0; i < kSamples; i++)
    {       
      reference_states.col(i) << state(0), state(1), state(2), 0, 0;
      //std::cout << "x :" <<state(0) << "y :" << state(1) << "z :" << state(2)<< '\n'; 
      reference_inputs.col(i) << 0,0,0;
      
    }
    //std::cout << "here in ref callback pt 2" << std::endl;
  }

  this->set_ref_params(reference_params);

  // std::cout << "atfer update 30 " << reference_params << std::endl;
  controller_.setReferenceStates(reference_states);
  controller_.setReferenceInputs(reference_inputs);
  controller_.setReferenceCBFParams(reference_params);  

 
  rclcpp::Time now = this->get_clock()->now();
  this->init_time = now;

  //std::cout << "set ref values" << std::endl;

  controller_.run();
  //std::cout << "ran the controller" << std::endl;
  // publish control and predicted path
  //publishControl();
  publishReference();
  publishPrediction();

  end_time = this->get_clock()->now();
  
  total_time = (end_time - start_time).nanoseconds();
  //std::cout << " total_time " << total_time << std::endl;

}


void NMPCControlNodelet::set_ref_params(Eigen::Matrix<double, kCBF_params, kSamples> &reference_params)
{

  //set first 3 rows with lane center x, y yaw
  double obj_x, obj_y, obj_theta, obj_vel, obj_length, obj_width;
  

  for(int i =0; i < vd_list.size(); ++i)
  { 
    obj_x = vd_list[i][0];
    obj_y = vd_list[i][1];
    obj_theta = vd_list[i][2];
    obj_vel = vd_list[i][3];   
    obj_length =  vd_list[i][4];
    obj_width = vd_list[i][5];

    //std::cout << "obj_x " << obj_x << "obj_y " << obj_y << "obj_theta " << obj_theta << "obj_vel " << obj_vel << "obj_length " << obj_length <<  "obj_width " << obj_width << std::end;
    reference_params.block((PARAM_WINDOW*i + INPUT_OFFSET),0 , PARAM_WINDOW, kSamples) = (Eigen::Matrix<double, PARAM_WINDOW, 1> () << 
                                                                              obj_x, 
                                                                              obj_y, 
                                                                              obj_theta, 
                                                                              obj_vel,
                                                                              obj_length, 
                                                                              obj_width).finished().replicate(1, kSamples);
    //std::cout << "saved params______________" << std::endl;
                                                                              
  }

  //std::cout << "ref params " << reference_params << std::endl; 
  
  
}


void NMPCControlNodelet::VD_list_callback(const vd_msgs::msg::VDList::SharedPtr VD_list_msg)
{ 
  auto iterator = VD_list_msg->vdlist.begin();
  this->vd_list.clear();
  

  while (iterator != VD_list_msg->vdlist.end())
  {
    this->vd_list.push_back({iterator->x, iterator->y, iterator->psi, iterator->velocity, iterator->length, iterator->width});
    //std::cout << iterator->x << iterator->y << iterator->yaw << iterator->length << iterator->width << std::endl;
    ++iterator;
  } 
  }

  


void NMPCControlNodelet::odomCallback(const vd_msgs::msg::VDpose::SharedPtr odom_msg)
{
  Eigen::Matrix<double, kStateSize, 1> state;
  //rame_id_ = odom_msg->header.frame_id;
  state(0) = odom_msg->x;
  state(1) = odom_msg->y;
  state(2) = odom_msg->psi;
  state(3) = odom_msg->velocity;
  
  // std::cout << " " <<  state << std::endl; 
  // std::cout << "odometery state" <<  state << std::endl;    
  this->vd_current_state = state;
  controller_.setState(state);
}



// void NMPCControlNodelet::publishControl()
// { 
//   //std::cout << "here inside control" << std::endl;
//   Eigen::Matrix<double, kInputSize, 1> pred_input = controller_.getPredictedInput();
  

//   vd_msgs::msg::VDControlCMD vd_control_msg;
//   vd_control_msg.velocity = this->ref_vel;
//   vd_control_msg.acceleration = pred_input(0);  
//   vd_control_msg.steering_angle = (pred_input(1) + pred_input(2))/(2 * 0.7);
//   pub_vd_cmd_->publish(vd_control_msg); 
// }



void NMPCControlNodelet::publishReference()
{
  Eigen::Matrix<double, kStateSize, kSamples> reference_states = controller_.getReferenceStates();  
  nav_msgs::msg::Path path_msg;
  path_msg.header.stamp = clock_.now();
  path_msg.header.frame_id = frame_id_;
  geometry_msgs::msg::PoseStamped pose;
  // std::cout << " " << std::endl;
  //std::cout << "Ref values here" << std::endl;

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
  pub_ref_traj_->publish(path_msg);
}


void NMPCControlNodelet::publishPrediction()
{
  Eigen::Matrix<double, kStateSize, kSamples> reference_states = controller_.getPredictedStates();
  Eigen::Matrix<double, kInputSize, kSamples> pred_input = controller_.getPredictedInput();


  vd_msgs::msg::VDtraj path_msg;
  // path_msg.header.stamp = clock_.now();
  // path_msg.header.frame_id = frame_id_;
  vd_msgs::msg::VDpose pose; 

  // std::cout << " " << std::endl;
  //std::cout << "Predicted values here" << std::endl;
  for (int i=0; i < kSamples; i++)
  { 
    
    pose.x = reference_states(0,i);
    pose.y = reference_states(1, i);
    pose.psi = reference_states(2, i);
    pose.velocity = reference_states(3, i);
    pose.distance = reference_states(4, i);
    pose.acceleration = pred_input(0, i);
    pose.steering_angle = (pred_input(1,i) + pred_input(2,i))/2;  
    
    //std::cout << this->init_time << std::endl; 
    //rclcpp::Duration dt = rclcpp::Duration::from_seconds((i+1) * this->Tf);
    //rclcpp::Time temp = this->init_time + dt;
    //pose.header.stamp.sec = this->init_time + (i+1.0) * this->Tf/ N;

    // Inside your loop
    rclcpp::Duration dt = rclcpp::Duration::from_seconds((i+1.0) * this->Tf / N);

    // Add duration to init_time
    rclcpp::Time temp = this->init_time + dt;

    // Convert to ROS message type
    pose.header.stamp = temp;  // ✅ if your ROS2 version has to_msg()


    //std::cout << "time sec " << pose.header.stamp.sec <<  " nanosec "<< pose.header.stamp.nanosec << " predx " << pose.x << " pred_y " << pose.y << " pred_yaw " << pose.psi << " pred_vel " << pose.velocity <<  " accel "<< pose.acceleration  << " steer "  << pose.steering_angle   << std::endl; 
   
    // auto temp = this->init_time  + (i+1) * this->Tf;
    // pose.header.stamp = temp;   //rclcpp::Duration::from_seconds(
    // std::cout << "pose.time_stamp.sec" << pose.time_stamp.sec << std::endl;
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