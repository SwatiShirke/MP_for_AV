#!/bin/bash
echo ""
echo "building ackerman nmpc planner"
cd ../../..


source install/setup.bash

cd src/MP_for_AV/vd_config/config
config_file="main_config.yaml" 
vd_params_path=$(yq e '.config_paths.vd_path' $config_file)
control_params_path=$(yq e '.config_paths.controller_path' $config_file)

cd ../..
cd vd_local_planner/scripts
source ~/acados/mpcenv/bin/activate

python3 acados_controller.py $vd_params_path $control_params_path

cd ..
cp scripts/c_generated_code/ackerman_model_model/ackerman_model_model.h include/vd_local_planner
cp scripts/c_generated_code/acados_solver_ackerman_model.h include/vd_local_planner


cd scripts
python3 gen_CBF_solver.py
g++ -fPIC -shared cbf_solver.cpp -o libcbf_solver.so
cd ..

cp scripts/cbf_solver.cpp src
cp scripts/cbf_solver.h include/vd_local_planner

cd ../../.. 
colcon build --packages-select vd_local_planner
# source install/setup.bash



