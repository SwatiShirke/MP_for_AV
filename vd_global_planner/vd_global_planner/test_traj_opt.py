import numpy as np
import osqp
from scipy import sparse

def optimize_speed_and_accel(waypoints, v_min, v_max_init, a_min, a_max, ay_max, eps=1e-6,
                              wv=1.0, wa=1e-3, wj=1.0, dt=0.1):
    N = waypoints.shape[0]
    n_vars = N + (N - 1)  # velocities + accelerations
    
    # ----- Step 1: Curvature-based velocity caps -----
    v_max = np.copy(v_max_init)
    for i in range(N):
        kappa = waypoints[i, 3]  # assuming curvature is in col 3
        v_curve = np.sqrt(ay_max / (abs(kappa) + eps))
        if v_curve < v_max[i]:
            v_max[i] = v_curve
    
    # ----- Step 2: Cost matrix P -----
    # Velocities block
    P_v = wv * sparse.eye(N)
    # Accelerations block (penalize accel + jerk)
    # First difference for jerk: size (N-2)x(N-1)
    e = np.ones(N - 1)
    D_jerk = sparse.diags([ -e[:-1], e[1:] ], [0, 1], shape=(N - 2, N - 1))
    P_a = wa * sparse.eye(N - 1) + wj * (D_jerk.T @ D_jerk)
    
    # Block diagonal
    P = sparse.block_diag([P_v, P_a], format='csc')
    
    # ----- Step 3: Linear term q -----
    v_target = v_max  # here target = max allowed speed
    q_v = -wv * v_target
    q_a = np.zeros(N - 1)
    q = np.hstack([q_v, q_a])
    
    # ----- Step 4: Constraints -----
    A_blocks = []
    l_list, u_list = [], []
    
    # 4.1 Dynamics constraints: v_{i+1} - v_i - dt*a_i = 0
    Av = sparse.diags([-np.ones(N - 1), np.ones(N - 1)], [0, 1], shape=(N - 1, N))
    Aa = sparse.diags([-dt * np.ones(N - 1)], [0], shape=(N - 1, N - 1))
    A_dyn = sparse.hstack([Av, Aa])
    A_blocks.append(A_dyn)
    l_list.append(np.zeros(N - 1))
    u_list.append(np.zeros(N - 1))
    
    # 4.2 Velocity bounds
    Av_bounds = sparse.hstack([sparse.eye(N), sparse.csc_matrix((N, N - 1))])
    A_blocks.append(Av_bounds)
    l_list.append(np.full(N, 0))
    u_list.append(v_max)
    
    # 4.3 Acceleration bounds
    Aa_bounds = sparse.hstack([sparse.csc_matrix((N - 1, N)), sparse.eye(N - 1)])
    A_blocks.append(Aa_bounds)
    l_list.append(np.full(N - 1, a_min))
    u_list.append(np.full(N - 1, a_max))
    
    # Stack everything
    A = sparse.vstack(A_blocks).tocsc()
    l = np.hstack(l_list)
    u = np.hstack(u_list)
    
    # ----- Step 5: Solve -----
    prob = osqp.OSQP()
    prob.setup(P=P, q=q, A=A, l=l, u=u, verbose=False)
    res = prob.solve()
    
    v_opt = res.x[:N]
    a_opt = res.x[N:]
    
    # Update waypoints with optimized values
    waypoints[:, -1] = v_opt
    return v_opt, a_opt
