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

