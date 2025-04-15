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

    dist = ca.norm_2(point1 - point2)  

    const1 = A_pl @ point1 - B_pl   
    const2 = A_obs @ point2 - B_obs
    g = ca.vertcat(const1, const2)

    nlp = {'f': dist, 'x': x, 'g' : g , 'p' : p }
    solver = ca.nlpsol('solver', 'ipopt', nlp) 
    solver.generate_dependencies('cbf_solver.cpp')

    # f = ca.Function('cbf_solver', [A_pl, B_pl, A_obs, B_obs], [dist]) 
    # f.generate('gen.cpp')
    # print(open('gen.cpp','r').read())

export_nlp_solver()











    



    



