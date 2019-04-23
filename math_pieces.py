import numpy as np
import logging
import datetime as dt
import sys
import pandas as pd
import scipy as sc


def interpolate(array_to_interpolate):  # y = self.df.iloc[0, 4:-2]
    xp = np.linspace(360, 740, 39)
    x = np.linspace(360, 740, 77)
    return np.interp(x, xp, array_to_interpolate)


def calculate_xyz(esl, fi_lambda_row):
    # numeric integrate: dx is always 5nm.. y=fi_lambda*x_overline
    dx = 5
    X, Y, Z, i = 0, 0, 0, 0
    for element in fi_lambda_row:
        X += element * esl.x_overline.values[i] * dx
        Y += element * esl.y_overline.values[i] * dx
        Z += element * esl.z_overline.values[i] * dx
        i += 1
    XYZ = X + Y + Z
    x = X / XYZ
    y = Y / XYZ
    z = Z / XYZ
    return [X, Y, Z, x, y, z]
