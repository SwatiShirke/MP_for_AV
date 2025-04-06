#!/bin/bash
echo ""
echo "building ackerman nmpc planner"
cd ../../..

source install/setup.bash
cd src/MP_for_AV/vd_local_planner
source ~/acados/mpcenv/bin/activate
cd scripts
python3 acados_controller.py 

cd ..
cp scripts/c_generated_code/ackerman_model_model/ackerman_model_model.h include/vd_local_planner
cp scripts/c_generated_code/acados_solver_ackerman_model.h include/vd_local_planner

cd ../../.. 
colcon build --packages-select vd_local_planner
source install/setup.bash



