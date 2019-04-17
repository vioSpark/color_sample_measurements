import numpy as np
import logging
import datetime as dt
import sys
import pandas as pd
import scipy as sc


class ExcelLoader:
    def __init__(self, excelpath='data/test.xls', logsfolder='data/logs/log'):
        logging.basicConfig(filename=logsfolder + str(dt.datetime.now().strftime("%Y-%m-%d_%H-%M")) + '.txt',
                            filemode='w',
                            format='%(asctime)s.%(msecs)-3d\t%(name)-20s\t%(levelname)-8s\t%(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)
        self.log = logging.getLogger(__name__)
        self.log.debug("log started")

        xlsx = pd.ExcelFile(excelpath)
        self.df = xlsx.parse(sheet_name=0, header=0)
        xlsx.close()

