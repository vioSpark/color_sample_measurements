import numpy as np
import logging
import datetime as dt
import sys
import pandas as pd
import scipy as sc


class ExternalSourcesLoader:
    def __init__(self, file_path='data/CIE_xyz_T_D65.xlsx'):
        data = pd.read_excel(file_path, header=0, index_col=0)
        self.light = data.loc[:740, 'F(l)\nD65'].T
        self.x_overline = data.loc[:740, 'CIE_x(l)']
        self.y_overline = data.loc[:740, 'CIE_y(l)']
        self.z_overline = data.loc[:740, 'CIE_z(l)']
