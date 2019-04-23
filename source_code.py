import numpy as np
import logging
import datetime as dt
import sys
import pandas as pd
import scipy as sc

from excel_loader import ExcelLoader
from txt_loader import TextFileLoader
from external_sources_loader import ExternalSourcesLoader
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
        tau = pd.to_numeric(tl.df.loc[tl.df['measurement number'] == row[1][-1]].loc[row[1][-3]][:-1]).abs().values

        spectral_values = (pd.to_numeric(
            row[1][:-3] * esl.light) * tau) / 10000  # the /10000 because of the percentages
        fi_lambda = fi_lambda.append(spectral_values.append(row[1][-3:]), ignore_index=True)
    except KeyError as e:
        print(e)
print('fi_lambda done')

X_Y_Z_data = pd.DataFrame(columns=['X', 'Y', 'Z', 'x', 'y', 'z', 'Name', 'Gloss', 'measurement number'])
for row in fi_lambda.iterrows():
    # numeric integrate: dx is always 5nm.. y=fi_lambda*x_overline
    append_me = pc.calculate_xyz(esl, row[1][:-3])
    append_me = append_me + list(row[1][-3:].values)
    X_Y_Z_data.loc[len(X_Y_Z_data)] = append_me
L_a_b_data = pd.DataFrame(columns=['L', 'a', 'b', 'Name', 'Gloss', 'measurement number'])
Xn, Yn, Zn = pc.calculate_xyz(esl, esl.light)[:3]
for row in X_Y_Z_data.iterrows():
    X, Y, Z = row[1][:3]
    L = 116 * (Y / Yn) ** (1 / 3) - 16
    a = 500 * ((X / Xn) ** (1 / 3) - (Y / Yn) ** (1 / 3))
    b = 200 * ((Y / Yn) ** (1 / 3) - (Z / Zn) ** (1 / 3))
    append_me = [L, a, b] + list(row[1][-3:].values)
    L_a_b_data.loc[len(L_a_b_data)] = append_me
raise NotImplementedError('remove the exception handling from fi_lambda!!!!4!4!4!4')
