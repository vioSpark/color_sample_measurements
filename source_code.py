import numpy as np
import logging
import datetime as dt
import sys
import pandas as pd
import scipy as sc

from excel_loader import ExcelLoader
from txt_loader import TextFileLoader
from lightsource_loader import LightSourceLoader
import math_pieces as pc

el = ExcelLoader(['data/reflection_tests/test.xls', 'data/reflection_tests/test 2.xls'])
el.interpolate()
tl = TextFileLoader(['data/transmission_test/', 'data/transmission_test/'])
ll = LightSourceLoader()
fi_lambda = pd.DataFrame(index=el.df[['Name', 'Gloss']],
                         columns=np.linspace(360, 740, 77))  # results are stored in this
for row in el.df:
    pass
asd = 4
