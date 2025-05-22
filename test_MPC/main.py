
import time, os
import numpy as np
from acados_controller import *
from plotFcn import *
from tracks.readDataFcn import getTrack
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import ipdb
from utils import get_loc_list, warm_start

#read and track and interpolate
track = "line.txt"
[Sref, Xref, Yref, Yawref,Kapparef] = getTrack(track)
Xref_s = interp1d(Sref,Xref, kind='cubic', fill_value="extrapolate")
Yref_s = interp1d(Sref, Yref, kind='cubic', fill_value="extrapolate")
Yawref_s = interp1d(Sref, Yawref, kind='cubic', fill_value="extrapolate")

Tf = 10    # time step
N = 10     # prediction horizon
T = 1000.00  # maximum simulation time[s]
sref_N = 5  # reference for final reference progress
L = 2     # wheebase in m
W = 1
d_safe = 0.2
pl_margin = 0.1
KNN = 5

#load model
model, acados_solver, acados_integrator = acados_controller(N, Tf, L, pl_margin, d_safe, KNN )
#dimensions
nx = model.x.rows()
nu = model.u.rows()
ny = nx + nu
Nsim = int(T / Tf)

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
gamma = 0.5
gamma_array = np.array([ gamma**(i) for i in range(N)])
#x_obj = np.array([Xref[30], Yref[30], Yawref[30], Sref[30]])
x_obj = np.array([Xref[50], Yref[50] + 0.5, Yawref[30], Sref[30]])

#simulate
for i in range(Nsim):
    if simX[i, 3] > Sref[-1]:
        break
    
    #print("VD pose ", simX[i])
    object_list = get_loc_list( L, W, x_obj)
    hx_0, h_lambda_bot, h_lambda_obj = warm_start(L, W, simX[i], object_list )
    print("hx_0", (hx_0[0])) 
    print("h_lambda_bot", h_lambda_bot)
    print("h_lambda_obj", h_lambda_obj) 
    

    sref = s0 + sref_N  
    yref = np.zeros(80)                      # state 4, input - 3 + 41 lambda+omega input +for control - 30 params, gamma = 1
    for j in range(N):        
        sref_ij = s0 + (sref - s0) * j / N
        x_ref = Xref_s(sref_ij)
        y_ref = Yref_s(sref_ij)
        yaw_ref = Yawref_s(sref_ij)        
        yref[0:4] =[x_ref,y_ref,yaw_ref,sref_ij]
        if len(object_list):
            yref[7:12] = [object_list[0,0], object_list[0,1], object_list[0,2], object_list[0,3], object_list[0,4]]
            yref[12] = hx_0[0]
            yref[-1] = gamma_array[j] 
        acados_solver.set(j, "p", yref)
        
    x_ref = Xref_s(sref) 
    y_ref = Yref_s(sref)
    yaw_ref = Yawref_s(sref)
    yref_N = np.zeros(80)
    yref_N[0:4] = np.array([x_ref,y_ref,yaw_ref, sref])       
    acados_solver.set(N, "p", yref_N)
    acados_solver.set(0, "lbx", simX[i, :])
    acados_solver.set(0, "ubx", simX[i, :])
    
    u0 = np.zeros((44,1))
    u0[3:7] = h_lambda_bot[0]
    u0[7: 11] = h_lambda_obj[0]
    acados_solver.set(0, "u", u0)


    # solve ocp
    t = time.time()
    status = acados_solver.solve()
    if status != 0:
        print("acados returned status {} in closed loop iteration {}.".format(status, i))

    elapsed = time.time() - t

    
    #get solution
    simU[i, :] = acados_solver.get(0, "u")   
    #print("u")
    simX[i+1, :] = acados_integrator.simulate(x=simX[i, :], u=simU[i,:])

    s0 = simX[i+1, 3] #x0[4] #sref

    # manage timings
    tcomp_sum += elapsed
    if elapsed > tcomp_max:
        tcomp_max = elapsed
    
#Plot Results
tracked_traj = simX[0:i, :]
t = np.linspace(0.0, Nsim+1, Nsim+1)
plotRes(simX, simU, t)
plot_followed_traj(tracked_traj[:,0], tracked_traj[:,1], Xref, Yref, x_obj[0], x_obj[1], L, W)


# Print some stats
print("Average computation time: {}".format(tcomp_sum / Nsim))
print("Maximum computation time: {}".format(tcomp_max))
#print("Average speed:{}m/s".format(np.average(simX[:, 3])))
print("Lap time: {}s".format(Tf * Nsim ))
# avoid plotting when running on Travis
if os.environ.get("ACADOS_ON_CI") is None:
    plt.show()
