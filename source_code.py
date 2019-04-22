import numpy as np
import logging
import datetime as dt
import sys
import pandas as pd
import scipy as sc

from excel_loader import ExcelLoader
from txt_loader import TextFileLoader
from lightsource_loader import ExternalSourcesLoader
import math_pieces as pc

el = ExcelLoader(['data/reflection_tests/test.xls', 'data/reflection_tests/test 2.xls'])
el.interpolate()
tl = TextFileLoader(['data/transmission_test/', 'data/transmission_test/'])
esl = ExternalSourcesLoader()
fi_lambda = pd.DataFrame(columns=[*np.linspace(360, 740, 77), 'Name', 'Gloss',
                                  'measurement number'])  # results are stored in this
for row in el.df.iterrows():
    # fi_lambda.append(row * tl.df.loc[row['Name']] * ll.df, sort=False)
    try:
        tau = pd.to_numeric(tl.df.loc[tl.df['measurement number'] == row[1][-1]].loc[row[1][-3]][:-1]).values
        spectral_values = pd.to_numeric(row[1][:-3] * esl.light) * tau
        fi_lambda = fi_lambda.append(spectral_values.append(row[1][-3:]), ignore_index=True)
    except KeyError as e:
        print(e)
print('fi_lambda done')

X_Y_Z_datas = pd.DataFrame(columns=['X', 'Y', 'Z', 'Name', 'Gloss', 'measurement number'])
for row in fi_lambda.iterrows():
    X = 0
    Y = 0
    Z = 0
    pass

raise NotImplementedError('remove the exception handling from fi_lambda!!!!4!4!4!4')
