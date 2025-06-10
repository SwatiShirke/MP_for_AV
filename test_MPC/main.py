
import time, os
import numpy as np
from acados_controller import *
from plotFcn import *
from tracks.readDataFcn import getTrack
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import ipdb
from utils import get_loc_list, warm_start, print_cbf_constraints, get_dist_region_to_region 
from CBF_constraints import CBF_constraints 

#read and track and interpolate
track = "line.txt"
[Sref, Xref, Yref, Yawref,Kapparef] = getTrack(track)
Xref_s = interp1d(Sref,Xref, kind='cubic', fill_value="extrapolate")
Yref_s = interp1d(Sref, Yref, kind='cubic', fill_value="extrapolate")
Yawref_s = interp1d(Sref, Yawref, kind='cubic', fill_value="extrapolate")

Tf = 5  # time step
N = 10   # prediction horizon 
T = 10.00  # maximum simulation time[s]
sref_N = 10 # reference for final reference progress
L = 2     # wheebase in m
W = 1
d_safe = 5
pl_margin = 0.2 
KNN = 5 
#load model
model, acados_solver, acados_integrator = acados_controller(N, Tf, L, pl_margin, d_safe, KNN )
#dimensions
nx = model.x.rows() 
nu = model.u.rows()
#ng = model.con_g_expr.rows()
try: 
    nh = model.con_h_expr.rows() 
except:
    nh = 0 

ny = nx + nu 
Nsim = int(T / (Tf/N)) 
params_WINDOW = 6 
lambda_WINDOW = 8 
input_offset = 3
param_offset = nx + nu + 1 

# initialize data structs
simX = np.zeros((Nsim +1, nx))
simU = np.zeros((Nsim +1, nu))
x0 = np.array([Xref[0], Yref[0], Yawref[0], Sref[0]])
acados_solver.set(0, "lbx", x0)
acados_solver.set(0, "ubx", x0)
simX[0,:] = x0 
s0 = x0[3]
tcomp_sum = 0
tcomp_max = 0
ineterpol_exit_flag = False
gamma = 0.8
gamma_array = np.array([ gamma**(i+1) for i in range(N)])
#x_obj = np.array([Xref[30], Yref[30], Yawref[30], Sref[30]])
x_obj = np.array([Xref[100], Yref[100]+ 0.6,  Yawref[100], Sref[100]])
vel = 1
h_x0_list = []
CBF_obj = CBF_constraints( Tf/N, L, W , d_safe, pl_margin, nx, nu) 
vel_ref = 1 
#simulate
for i in range(Nsim):
    if simX[i, 3] > Sref[-1]:
        break    

    print(" ")
    object_list = get_loc_list( L, W, x_obj)
    #hx_0, h_lambda_bot, h_lambda_obj = warm_start(L, W, simX[i], object_list )
    hx_0, h_lambda_bot, h_lambda_obj = get_dist_region_to_region(L, W, simX[i], object_list)       
    print("hx_0", (hx_0[0])) 
    print("h_lambda_bot", h_lambda_bot)
    print("h_lambda_obj", h_lambda_obj) 
    h_x0_list.append(hx_0[0])    
    if hx_0[0] > d_safe:
        #hx_0[0] = 0
        h_lambda_bot = [np.zeros((4,1))]
        h_lambda_obj = [np.zeros((4,1))]
      
    # sref = s0 +   
    yref = np.zeros(80)                      # state 4, input - 3 + 41 lambda+omega input +for control - 30 params, gamma = 1
    #print("X_current", simX[i, :]) 

    for j in range(N):        
        sref_ij = s0 + vel_ref * Tf/N * (j) 
        x_ref = Xref_s(sref_ij)
        y_ref = Yref_s(sref_ij)
        yaw_ref = Yawref_s(sref_ij)        
        yref[0:5] =[x_ref,y_ref,yaw_ref,sref_ij, vel_ref]
        #print("yref[0:5]", yref[0:5])
        if len(object_list):
            if hx_0[0] > d_safe: 
                yref[param_offset: param_offset + params_WINDOW -1] = [0, 0, 0, 0, 0]
                yref[param_offset + params_WINDOW-1] = 0
                yref[-1] = 0 

            else:
                yref[param_offset: param_offset + params_WINDOW -1] = [object_list[0,0], object_list[0,1], object_list[0,2], object_list[0,3], object_list[0,4]]
                yref[param_offset + params_WINDOW-1] = hx_0[0]
                yref[-1] = gamma_array[j] 

        acados_solver.set(j, "p", yref)        
        u0 = np.zeros((44,1))
        #u0[1:3] = np.array([3.14, 3.14] ).reshape(2,1)
        u0[3:7] = h_lambda_bot[0].reshape(4,1)
        u0[7: 11] = h_lambda_obj[0].reshape(4,1)
        u0[-1] = 0.1 
        acados_solver.set(j, "u", u0) 

    sref_ij = s0 + vel * Tf          
    x_ref = Xref_s(sref_ij) 
    y_ref = Yref_s(sref_ij)
    yaw_ref = Yawref_s(sref_ij)
    yref_N = np.zeros(80)
    yref_N[0:4] = np.array([x_ref,y_ref,yaw_ref, sref_ij])  
    if len(object_list):
            yref_N[param_offset: param_offset + params_WINDOW-1] = [object_list[0,0], object_list[0,1], object_list[0,2], object_list[0,3], object_list[0,4]]
            yref_N[param_offset + params_WINDOW-1] = hx_0[0] 
            yref_N[-1] = gamma_array[j]     
    acados_solver.set(N, "p", yref_N)
    acados_solver.set(0, "lbx", simX[i, :])
    acados_solver.set(0, "ubx", simX[i, :]) 
        
    # solve ocp
    t = time.time()
    status = acados_solver.solve()
    elapsed = time.time() - t  

    #get solution
    u = acados_solver.get(0, "u") 
    simU[i, :] = u 

    for k in range(N):         
        u_current = acados_solver.get(k, "u") 
        x_current = acados_solver.get(k, "x") 
        params = acados_solver.get(k, "p") 
        h_list, h_lb_list, h_ub_list = CBF_obj.get_cbf_constraints(x_current, u_current, params) 
        #print_cbf_constraints( x_current, u_current, params, L, W, d_safe, Tf/N, nx, nu)
    vel =  u[0] 
    
    print("")
    print("u", u[0:3])
    print("vel", vel)
    simX[i+1, :] = acados_integrator.simulate(x=simX[i, :], u=simU[i,:])
    s0 = simX[i+1, 3] #x0[4] #sref
    
    tcomp_sum += elapsed
    if elapsed > tcomp_max:
        tcomp_max = elapsed

    if status != 0:
        print("acados returned status {} in closed loop iteration {}.".format(status, i))
        #break
   
#Plot Results
tracked_traj = simX[0:i, :]
t = np.linspace(0.0, Nsim+1, Nsim+1)
plotRes(simX, simU, t)
plot_followed_traj(tracked_traj[:,0], tracked_traj[:,1], Xref, Yref, x_obj[0], x_obj[1], L, W)
#plot_hx0(t[0:-1], np.array(h_x0_list).reshape(-1)  )

# Print some stats
print("Average computation time: {}".format(tcomp_sum / Nsim))
print("Maximum computation time: {}".format(tcomp_max))
#print("Average speed:{}m/s".format(np.average(simX[:, 3])))
print("Lap time: {}s".format(Tf * Nsim ))
# avoid plotting when running on Travis
if os.environ.get("ACADOS_ON_CI") is None:
    plt.show()
