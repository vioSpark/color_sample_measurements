import numpy as np
import logging
import datetime as dt
import sys
import pandas as pd
import scipy as sc
import os
import math_pieces as pc


class ExcelLoader:
    def __init__(self, files, logsfolder='data/logs/log'):
        """
        logging.basicConfig(filename=logsfolder + str(dt.datetime.now().strftime("%Y-%m-%d_%H-%M")) + '.txt',
                            filemode='w',
                            format='%(asctime)s.%(msecs)-3d\t%(name)-20s\t%(levelname)-8s\t%(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)
        self.log = logging.getLogger(__name__)
        self.log.debug("log started")
        """
        self.df = pd.DataFrame()
        meas_number = 0
        for file in files:
            self.df = self.df.append(self.read_excel(file)).fillna(meas_number)
            meas_number += 1

    @staticmethod
    def read_excel(excelpath='data/test.xls'):
        xlsx = pd.ExcelFile(excelpath)
        df = pd.DataFrame(columns=['measurement number']).append(
            xlsx.parse(sheet_name=0, header=0).drop(['No.', 'Date, Time', 'Mask', 'Comment'], axis=1))
        xlsx.close()
        return df

    def interpolate(self):
        data = []
        for row in self.df.iterrows():
            # [*pc.interpolate(pd.to_numeric(row[1][3:])),
            # *row[1][1:2] (this is name), *row[1][2:3] (Gloss (SCI/SCE)), *row[1][0:1] (measurement number)]
            data.append([*pc.interpolate(pd.to_numeric(row[1][3:])), *row[1][1:2], *row[1][2:3], *row[1][0:1]])
        self.df = pd.DataFrame(data, columns=[*np.linspace(360, 740, 77), *['Name', 'Gloss', 'measurement number']])
