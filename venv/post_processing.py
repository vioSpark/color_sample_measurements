import numpy as np
import pandas as pd


# this code is not debugged yet
def calculate_std_at_meas_0(df):
    initial_data = df["measurement number" == 0]

    # copied from the other function
    gloss_type = ('SCI', 'SCE')
    rt_type = ('Transmission', 'Reflection')
    temp_type = ('5', 'H')
    water_type = ('+', 'D', 'M')
    color_type = ('P', 'Z')
    for gloss in range(2):
        for rt in range(2):
            for temp in range(2):
                for water in range(3):
                    for color in range(2):
                        mask = (tmp.Gloss == gloss_type[gloss]) & \
                               (tmp.RT == rt_type[rt]) & \
                               (tmp.loc[:, 'Temperature'] == temp_type[temp]) & \
                               (tmp.loc[:, 'Water type'] == water_type[water]) & \
                               (tmp.loc[:, 'Color'] == color_type[color])
                        res = initial_data.loc[mask]
                        print(res)
