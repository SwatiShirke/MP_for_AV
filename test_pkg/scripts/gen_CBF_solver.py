import casadi as ca
import numpy as np

def export_nlp_solver():
    m_pl = 4
    n_pl = 2
    m_obs = 4
    n_obs = 2

    A_pl = ca.SX.sym("A_pl", m_pl, n_pl)
    B_pl = ca.SX.sym("B_pl", m_pl, 1)

    A_obs = ca.SX.sym("A_obs", m_obs, n_obs)
    B_obs = ca.SX.sym("B_obs", m_obs, 1 )

    point1 = ca.SX.sym('point1', n_pl,1)
    point2 = ca.SX.sym('point2', n_obs,1) 

    x = ca.vertcat(point1, point2) 
    p = ca.vertcat(
        ca.reshape(A_pl, -1, 1),
        ca.reshape(B_pl, -1, 1),
        ca.reshape(A_obs, -1, 1),
        ca.reshape(B_obs, -1, 1)
        )
    cost=0   
    dist_vec = point1-point2
    cost = dist_vec.T@dist_vec

    const1 = ca.mtimes(A_pl, point1) - B_pl   
    const2 = ca.mtimes(A_obs , point2)- B_obs
    g = ca.vertcat(const1, const2)

    nlp = {'f': cost, 'x': x, 'g' : g , 'p' : p }
    solver = ca.nlpsol('cbf_solver', 'ipopt', nlp) 
    #solver(lbg=-ca.inf,ubg=0)
    solver.generate("cbf_solver.cpp", {"with_header": True,  "cpp": True})

    
export_nlp_solver()











    



    



