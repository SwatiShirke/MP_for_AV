from casadi import *
from tracks.readDataFcn import getTrack
from acados_template import AcadosModel


def ackerman_model(L, track="LMS_Track.txt"):
    model_name = "ackerman_model"
    model = AcadosModel()   

    #states
    x_pos = SX.sym("x_pos")
    y_pos = SX.sym("y_pos")
    theta = SX.sym("theta")
    #psi = SX.sym("psi")
    s = SX.sym("s")
    x = vertcat(x_pos, y_pos, theta, s)

    
    #states dt
    x_pos_dt = SX.sym("x_pos_dt")
    y_pos_dt = SX.sym("y_pos_dt")
    theta_dt = SX.sym("theta_dt")
    #psi_dt = SX.sym("psi_dt")
    s_dt = SX.sym("s_dt")
    x_dot = vertcat(x_pos_dt, y_pos_dt, theta_dt, s_dt)

    #input 
    Vf = SX.sym("Vf")
    #steer_rate = SX.sym("steer_rate")
    steer_angle_in = SX.sym("steer_angle_in")
    steer_angle_out = SX.sym("steer_angle_out")
    delta = (steer_angle_in + steer_angle_out)/2
    u = vertcat(Vf, steer_angle_in, steer_angle_out)
    
    #system dynamics/kinematics
    f_expl =vertcat(Vf * np.cos(theta),
                    Vf * np.sin(theta),
                    Vf / L * np.tan(delta),
                    #steer_rate,
                    Vf )
    
    p = []

    model.f_impl_expr = x_dot - f_expl
    model.f_expl_expr = f_expl
    model.x = x
    model.xdot = x_dot
    model.u = u
    model.x0 = np.array([0.,0,0,0])
    # model.z = z
    model.p = p
    model.name = model_name

    return model