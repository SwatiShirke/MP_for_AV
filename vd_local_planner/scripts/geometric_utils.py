import numpy as np
import casadi as ca
# class Polytope():
#     def __init__(self, lenght, width, origin):
#         self.length = lenght
#         self.width = width
#         self.A_mat =  np.array([[-1, 0], [0, -1], [1, 0], [0, 1]])
#         x0, y0 = origin
#         self.B_mat = np.array([[ -x0 + self.length /2], [-y0 + self.width/2 ], [x0 + self.length /2], [y0 + self.width/2]])

#     def get_poly_mat(self):
#         return self.A_mat, self.B_mat

#     def get_poly_mat(self, origin):
#         x0, y0 = origin
#         self.B_mat = np.array([[ -x0 + self.length /2], [-y0 + self.width/2 ], [x0 + self.length /2], [y0 + self.width/2]])
#         return self.A_mat, self.B_mat
    

def get_polytopes(no_obj, obj_data_list):
    #vd_geo - (x,y, theta, length, width)
    #obj_list = [(x,y, theta, length, width)]
    mat_obj_list = [] 
    x,y,_, l,w = obj_data_list[0] 
    vd_obj = VD_polytope(l, w)
    mat_obj_list.append(vd_obj)

    for i in range(1,no_obj+1):
        x, y, _, l, w = obj_data_list[i]
        obj = Polytope((x,y),l, w)
        mat_obj_list.append(obj) 
    return mat_obj_list 


class Polytope():    
    def __init__(self,origin, L , W):
        self.origin_x = origin[0]
        self.origin_y = origin[1]        
        self.length = L
        self.width = W
        
    def get_matrices(self):
        mat_A = np.array([[-1, 0], [0, -1], [1, 0], [0, 1]])
        vec_b = np.array([[-self.origin_x+self.length/2], [-self.origin_y+self.width/2], [self.origin_x+self.length/2], [self.origin_y+self.width/2]])
        return mat_A, vec_b
    
class VD_polytope():
    def __init__(self, L, W):
        self.A = np.array([[-1, 0], [0, -1], [1, 0], [0, 1]])
        self.B = np.array([[-L/2], [-W/2], [L/2], [W/2]])

    def get_matrices(self):
        return self.A, self.B
    
        
