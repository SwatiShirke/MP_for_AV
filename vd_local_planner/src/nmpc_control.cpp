#include "vd_local_planner/nmpc_control.h"

namespace nmpc_control_nodelet
{

NMPCControl::NMPCControl()
  : current_state_(Eigen::Matrix<double, kStateSize, 1>::Zero()),
    reference_states_(Eigen::Matrix<double, kStateSize, kSamples>::Zero()),
    reference_inputs_(Eigen::Matrix<double, kInputSize, kSamples>::Zero()),
    predicted_states_(Eigen::Matrix<double, kStateSize, kSamples>::Zero()),
    predicted_inputs_(Eigen::Matrix<double, kInputSize, kSamples>::Zero()),
    reference_cbf_params_(Eigen::Matrix<double, kCBF_params, kSamples>::Zero()),
    init_inputs_(Eigen::Matrix<double, kInputSize, kSamples>::Zero()), 
    solve_from_scratch_(true) 
{
 
}

void NMPCControl::setState(const Eigen::Matrix<double, kStateSize, 1> &state) { current_state_.block(0, 0, 4, 1) = state.block(0, 0, 4, 1); }
//void NMPCControl::setOmega(const Eigen::Matrix<double, 3, 1> &omega) { current_state_.block(10, 0, 3, 1) = omega; }
void NMPCControl::setReferenceStates(const Eigen::Matrix<double, kStateSize, kSamples> &reference_states) { reference_states_ = reference_states; }
void NMPCControl::setReferenceInputs(const Eigen::Matrix<double, kInputSize, kSamples> &reference_inputs) { reference_inputs_ = reference_inputs; }
void NMPCControl::setReferenceCBFParams(const Eigen::Matrix<double, kCBF_params, kSamples> &reference_cbf_params) { reference_cbf_params_ = reference_cbf_params; }
void NMPCControl::setInitInputs(const Eigen::Matrix<double, kInputSize, kSamples> &init_inputs) {init_inputs_ = init_inputs;};
void NMPCControl::setMass(double mass) { wrapper_.setMass(mass); }
void NMPCControl::setGravity(double gravity) { wrapper_.setGravity(gravity); }

Eigen::Matrix<double, kStateSize, 1> NMPCControl::getPredictedState() { return predicted_states_.col(1);  }
Eigen::Matrix<double, kInputSize, 1> NMPCControl::getPredictedInput() { return predicted_inputs_.col(0);  }
Eigen::Matrix<double, kStateSize, kSamples> NMPCControl::getPredictedStates() { return predicted_states_; }
Eigen::Matrix<double, kStateSize, kSamples> NMPCControl::getReferenceStates() { return reference_states_; }
Eigen::Matrix<double, kInputSize, kSamples> NMPCControl::getReferenceInputs() { return reference_inputs_; }
//Eigen::Matrix<double, kCBF_params, kSamples> NMPCControl::getReferenceCBFParams() {return reference_cbf_params_;}

void NMPCControl::run()
{  wrapper_.setTrajectory(reference_states_, reference_inputs_, reference_cbf_params_);

    if (solve_from_scratch_)
  {
    std::cout << "Solving NMPC with initial guess.\n";
    wrapper_.prepare(current_state_, init_inputs_);
    solve_from_scratch_ = false;
  }

  bool solved = wrapper_.update(current_state_);
  if (!solved)
    std::cout << "NMPC could not find a solution.";

  wrapper_.getStates(predicted_states_);
  wrapper_.getInputs(predicted_inputs_);
}

}