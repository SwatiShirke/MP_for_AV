
import time, os
import numpy as np
from acados_controller import *
from plotFcn import *
from tracks.readDataFcn import getTrack
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import ipdb


#read and track and interpolate
track = "sine.txt"
[Sref, Xref, Yref, Yawref,Kapparef] = getTrack(track)
Xref_s = interp1d(Sref,Xref, kind='cubic', fill_value="extrapolate")
Yref_s = interp1d(Sref, Yref, kind='cubic', fill_value="extrapolate")
Yawref_s = interp1d(Sref, Yawref, kind='cubic', fill_value="extrapolate")

Tf = 10    # time step
N = 10     # prediction horizon
T = 500.00  # maximum simulation time[s]
sref_N = 10  # reference for final reference progress
L = 1.5     # wheebase in m

#load model
model, acados_solver, acados_integrator = acados_controller(N, Tf, L )
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

#simulate
for i in range(Nsim):
    if simX[i, 3] > Sref[-1]:
        break
    # update reference    
    # if i == 0: 
    #     vel = simU[0, 0] 
    # else:
    #     vel = simU[i-1, 0]     
    #sref = s0 + (vel * Tf * N)  #for velocity based prediction 
    
    sref = s0 + sref_N           #for distance based prediction
    for j in range(N):        
        sref_ij = s0 + (sref - s0) * j / N
        x_ref = Xref_s(sref_ij)
        y_ref = Yref_s(sref_ij)
        yaw_ref = Yawref_s(sref_ij)
        yref=np.array([x_ref,y_ref,yaw_ref,sref_ij, 0, 0, 0])
        acados_solver.set(j, "yref", yref)

        
    x_ref = Xref_s(sref)
    y_ref = Yref_s(sref)
    yaw_ref = Yawref_s(sref)
    yref_N = np.array([x_ref,y_ref,yaw_ref, sref])       
    acados_solver.set(N, "yref", yref_N)
    acados_solver.set(0, "lbx", simX[i, :])
    acados_solver.set(0, "ubx", simX[i, :])
    # solve ocp
    t = time.time()
    status = acados_solver.solve()
    if status != 0:
        print("acados returned status {} in closed loop iteration {}.".format(status, i))

    elapsed = time.time() - t

    # get solution
    #simX[i, :] = acados_solver.get(0, "x")
    simU[i, :] = acados_solver.get(0, "u")
        
    #print("u")
    simX[i+1, :] = acados_integrator.simulate(x=simX[i, :], u=simU[i,:])

    #print(acados_solver.get_cost())
    #print(simU[i, :])
    #print("predicted")
    #print(simX[i+1, :])
    s0 = simX[i+1, 3] #x0[4] #sref

    # manage timings
    tcomp_sum += elapsed
    if elapsed > tcomp_max:
        tcomp_max = elapsed

    
#Plot Results
tracked_traj = simX[0:i, :]
t = np.linspace(0.0, Nsim+1, Nsim+1)
plotRes(simX, simU, t)
plot_followed_traj(tracked_traj[:,0], tracked_traj[:,1], Xref, Yref)


# Print some stats
print("Average computation time: {}".format(tcomp_sum / Nsim))
print("Maximum computation time: {}".format(tcomp_max))
#print("Average speed:{}m/s".format(np.average(simX[:, 3])))
print("Lap time: {}s".format(Tf * Nsim ))
# avoid plotting when running on Travis
if os.environ.get("ACADOS_ON_CI") is None:
    plt.show()
