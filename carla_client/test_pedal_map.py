import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata
# Load your Excel data


def interpolate_pedal(vel_query, accel_query, path):
    df = pd.read_csv(path)  

    points = np.column_stack((df['velocity'].values, df['acceleration'].values))       
    values = df['pedal'].values

    query_points = np.column_stack((vel_query, accel_query))

    pedals_interp = griddata(points, values, query_points, method='cubic')
    # if np.isnan(pedals_interp):
    #     pedals_interp = griddata(points, values, query_points, method='nearest')

    return pedals_interp




if __name__ == '__main__':
    path = 'pedal_map_data.xlsx'
    vel_query, accel_query = 3.5, -4.0487
    ff_cmd = interpolate_pedal(vel_query, accel_query, path)

    print("ff_cmd", ff_cmd)