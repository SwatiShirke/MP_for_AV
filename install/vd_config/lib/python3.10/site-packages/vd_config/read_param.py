from dataclasses import dataclass 
import yaml
import inspect

@dataclass
class VD_params:
    lf : float  #dist from center to front axel
    lr : float  #dist from center to rear axel
    track_width : float  #trackwidth
    mass : float #kg

@dataclass
class Controller_params:
    N : int
    Tf : float
    polytope_margin : float # in meters, polytope margin 
    d_safe : float    #safe distance between 2 polytopes can be >= 0 

@dataclass
class Planner_params:
    grid_res : float # grid resolution in meters 
    buffer_grid : int # no of buffer grids added on each side of grid map



class read_params():
    def __init__(self):
        self.type = None
        self.path = None
        self.type_dict = ["VD_params", "controller_params", "planner_params"] 

    def read_yaml(self, file_path):
        with open(file_path, 'r') as file:
            try:
                parsed_yaml = yaml.safe_load(file)
                return parsed_yaml
            except yaml.YAMLError as exc:
                print(exc)
                return None

    def dict_to_class(self, clss, clss_name, data): # here clss is the name of the Class e.g MpcQuadrotor
        return clss(
            **{
            key: (data[key] if (val.default == val.empty)&(key in data) else data.get(key, val.default))
            for key, val in inspect.signature(clss_name).parameters.items()
            }
        ) 


    def read_params(self, file_path, file_type):
        if (file_path== None):
            print("missing filepath")           
        elif file_path == None or file_type not in self.type_dict:

            print("missing file type or not allowed one. Type should be be one the following :")
            print(self.type_dict)
        
        else:
            if file_type == "VD_params":
                params = self.read_vd_param(file_path)

            elif file_type ==  "controller_params":
                params = self.read_controller_param(file_path)

            elif file_type == "planner_params":
                params = self.read_planner_param(file_path)

            else:
                print("Reading function not implemented for the given file type!!")

        return params    

    def read_controller_param(self, file_path):
        param_dict = self.read_yaml(file_path)
        class_type = Controller_params
        if param_dict == None:
            return None
        else:
            control_class = self.dict_to_class(class_type, class_type, param_dict)
            return control_class

    def read_planner_param(self, file_path):
        param_dict = self.read_yaml(file_path)
        class_type = Planner_params
        if param_dict == None:
            return None
        else:
            planner_class = self.dict_to_class(class_type, class_type, param_dict)
            return planner_class
 
    def read_vd_param(self, file_path):
        param_dict = self.read_yaml(file_path)
        class_type = VD_params
        if param_dict == None:
            return None
        else:
            vd_class = self.dict_to_class(class_type, class_type, param_dict)
            print(vd_class.lf)
            return vd_class