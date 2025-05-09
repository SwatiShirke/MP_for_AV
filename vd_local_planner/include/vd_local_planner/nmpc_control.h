#ifndef NMPC_CONTROL_H
#define NMPC_CONTROL_H
#include <vd_local_planner/wrapper.h>
#include <math.h>
#include <boost/array.hpp>
#include <yaml-cpp/yaml.h>
#include <ctime>
#include <iostream>

namespace nmpc_control_nodelet
{
class NMPCControl
{
public:
  NMPCControl();
  void setState(const Eigen::Matrix<double, kStateSize, 1> &state);
  void setOmega(const Eigen::Matrix<double, 3, 1> &omega);
  void setReferenceStates(const Eigen::Matrix<double, kStateSize, kSamples> &reference_states);
  void setReferenceInputs(const Eigen::Matrix<double, kInputSize, kSamples> &reference_inputs);
  void setReferenceCBFParams(const Eigen::Matrix<double, kCBF_params, kSamples> &reference_cbf_params);
  void setInitInputs(const Eigen::Matrix<double, kInputSize, kSamples> &init_inputs);

  Eigen::Matrix<double, kStateSize, 1> getState() {return current_state_;}
  void setMass(double mass);
  void setGravity(double gravity);
  Eigen::Matrix<double, kStateSize, 1> getPredictedState();
  Eigen::Matrix<double, kInputSize, 1> getPredictedInput();
  Eigen::Matrix<double, kStateSize, kSamples> getPredictedStates();
  Eigen::Matrix<double, kStateSize, kSamples> getReferenceStates();
  Eigen::Matrix<double, kInputSize, kSamples> getReferenceInputs();
  

  void run();

  EIGEN_MAKE_ALIGNED_OPERATOR_NEW
private:
  bool solve_from_scratch_;
  Eigen::Matrix<double, kStateSize, 1> current_state_;
  Eigen::Matrix<double, kStateSize, kSamples> reference_states_;
  Eigen::Matrix<double, kInputSize, kSamples> reference_inputs_;
  Eigen::Matrix<double, kStateSize, kSamples> predicted_states_;
  Eigen::Matrix<double, kInputSize, kSamples> predicted_inputs_;
  Eigen::Matrix<double, kCBF_params, kSamples> reference_cbf_params_;
  Eigen::Matrix<double, kInputSize, kSamples> init_inputs_;
  NMPCWrapper wrapper_;
};

}
#endif