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

el = ExcelLoader(
    ['data/reflection_tests_2/SZIE_2019_01_23.xls', 'data/reflection_tests_2/SZIE_2019_02_27.xls',
     'data/reflection_tests_2/SZIE_2019_03_13.xls', 'data/reflection_tests_2/SZIE_2019_03_27.xls',
     'data/reflection_tests_2/SZIE_2019_04_24.xls', ])
el.interpolate()
tl = TextFileLoader(['data/transmission_test_2/1/', 'data/transmission_test_2/2/', 'data/transmission_test_2/3/',
                     'data/transmission_test_2/4/', 'data/transmission_test_2/5/', ])
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
        # !!!!!!!!!! change the commented line, to ignore inconsistencies !!!!!!!!!!
        # print(e)
        raise e
fi_lambda.to_csv()
print('fi_lambda saved')

X_Y_Z_data = pd.DataFrame(columns=['X', 'Y', 'Z', 'x', 'y', 'z', 'Name', 'Gloss', 'measurement number'])
for row in fi_lambda.iterrows():
    # numeric integrate: dx is always 5nm.. y=fi_lambda*x_overline
    append_me = pc.calculate_xyz(esl, row[1][:-3])
    append_me = append_me + list(row[1][-3:].values)
    X_Y_Z_data.loc[len(X_Y_Z_data)] = append_me
X_Y_Z_data.to_csv()
print('X, Y, Z data saved')

L_a_b_data = pd.DataFrame(columns=['L', 'a', 'b', 'Name', 'Gloss', 'measurement number'])
Xn, Yn, Zn = pc.calculate_xyz(esl, esl.light)[:3]
for row in X_Y_Z_data.iterrows():
    X, Y, Z = row[1][:3]
    L = 116 * (Y / Yn) ** (1 / 3) - 16
    a = 500 * ((X / Xn) ** (1 / 3) - (Y / Yn) ** (1 / 3))
    b = 200 * ((Y / Yn) ** (1 / 3) - (Z / Zn) ** (1 / 3))
    append_me = [L, a, b] + list(row[1][-3:].values)
    L_a_b_data.loc[len(L_a_b_data)] = append_me
L_a_b_data.to_csv()
print('L, a, b data saved')

names = set(L_a_b_data['Name'])
delta = []
for name in names:
    # hardcoded SCE
    mask = (L_a_b_data.Name == name) & (L_a_b_data.Gloss == 'SCE')
    delta_Lab = (L_a_b_data[mask].sort_values('measurement number')).iloc[:, 0:3].diff()[1:]
    diffs = list(delta_Lab.applymap(lambda x: x ** 2).sum(1).apply(np.sqrt))
    diffs.extend([name, 'SCE'])
    delta.append(diffs)

    # hardcoded SCI
    mask = (L_a_b_data.Name == name) & (L_a_b_data.Gloss == 'SCI')
    delta_Lab = (L_a_b_data[mask].sort_values('measurement number')).iloc[:, 0:3].diff()[1:]
    diffs = list(delta_Lab.applymap(lambda x: x ** 2).sum(1).apply(np.sqrt))
    diffs.extend([name, 'SCI'])
    delta.append(diffs)
final_final_delta_master_values_v3 = pd.DataFrame(delta)
final_final_delta_master_values_v3.to_csv()
print('final delta values saved')
