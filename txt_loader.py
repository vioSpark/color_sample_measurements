import numpy as np
import logging
import datetime as dt
import sys
import os
import pandas as pd
import scipy as sc
import math
import math_pieces as pc


class TextFileLoader:
    def __init__(self, dirs):
        self.df = pd.DataFrame(columns=['measurement number'])
        meas_number = 0
        for directory in dirs:
            self.df = self.df.append(self.read_dir(directory))
            self.df.fillna(meas_number, inplace=True)
            meas_number += 1

    def read_dir(self, path='data/transmission_test/'):
        df = pd.DataFrame()
        index = []

        files = os.scandir(path)
        for file in files:
            df = df.append(self.read_file(file))
            index.append(str(file).split("'")[1].split('.')[0])
        df.index = index
        return df

    @staticmethod
    def read_file(file_path='data/test.txt'):
        text = open(file_path, mode='r').readlines()[6:]
        header = text[0].split('\t')
        header[3] = 'Trans(percentT)'
        header[5] = 'Energy(100percentT)'
        header[6] = 'Energy(0percentT)'

        data = []
        for row in text[1:]:
            data.append(row.split('\t'))
        row = pd.DataFrame(data, columns=None).drop([2, 5, 8], axis=1).T
        real_header = row.iloc[1, :]
        row.columns = real_header
        return row.loc[4, :]
