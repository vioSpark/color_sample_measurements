import numpy as np
import logging
import datetime as dt
import sys
import pandas as pd
import scipy as sc


class TextFileLoader:
    def __init__(self, file_path='data/test.txt'):
        text = open(file_path, mode='r').readlines()[6:]
        header = text[0].split('\t')
        header[3] = 'Trans(percentT)'
        header[5] = 'Energy(100percentT)'
        header[6] = 'Energy(0percentT)'

        data = []
        for row in text[1:]:
            data.append(row.split('\t'))
        self.df = pd.DataFrame(data, columns=None).drop([2, 5, 8], axis=1).T
        # self.df.index = header
        real_header = self.df.iloc[1, :]
        self.df.columns = real_header
        # self.df=self.df.drop(['Wavelength(nm)'], axis=0)
        raise NotImplementedError('which column to select?')
        self.df = self.df.loc[:,2]

    @staticmethod
    def interpolate(array_to_interpolate):
        xp = np.linspace(360, 740, 39)
        x = np.linspace(360, 740, 77)
        return np.interp(x, xp, array_to_interpolate)
