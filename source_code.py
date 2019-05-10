import numpy as np
import logging
import datetime as dt
import sys
import pandas as pd
import scipy as sc

from excel_loader import ExcelLoader
from txt_loader import TextFileLoader
from external_sources_loader import ExternalSourcesLoader
from visualiser import Transformer
import math_pieces as pc

el = ExcelLoader(
    ['data/final_export/excel_folder/SZIE_2018_11_15.xls'])
el.interpolate()
tl = TextFileLoader(
    ['data/final_export/2018-11-15/'])
esl = ExternalSourcesLoader()
fi_lambda = pd.DataFrame(columns=[*np.linspace(360, 740, 77), 'Name', 'RT', 'Gloss',
                                  'measurement number'])  # results are stored in this
# //R/T is added
for row in el.df.iterrows():
    # fi_lambda.append(row * tl.df.loc[row['Name']] * ll.df, sort=False)
    try:
        tau = tl.df.loc[tl.df['measurement number'] == row[1][-1]].loc[row[1][-3]][:-1].str.replace(',', '').astype(
            float).abs().values
        # tau = pd.to_numeric(tl.df.loc[tl.df['measurement number'] == row[1][-1]].loc[row[1][-3]][:-1]).abs().values

        spectral_values_1 = (pd.to_numeric(
            row[1][:-3] * esl.light)) / 100  # the /100 because of the percentages
        spectral_values_2 = (esl.light * tau) / 100  # the /100 because of the percentages
        fi_lambda = fi_lambda.append(spectral_values_1.append(row[1][-3:]), ignore_index=True)
        fi_lambda.iloc[-1, -3] = 'Reflection'
        fi_lambda = fi_lambda.append(spectral_values_2.append(row[1][-3:]), ignore_index=True)
        fi_lambda.iloc[-1, -3] = 'Transmission'

    except KeyError as e:
        # !!!!!!!!!! change the commented line, to ignore inconsistencies !!!!!!!!!!
        # print(e)
        try:
            if e.args[0].find('ZS') >= 0:
                tau = pd.to_numeric(
                    tl.df.loc[tl.df['measurement number'] == row[1][-1]].loc[row[1][-3].replace('ZS', 'SZ')][:-1]) \
                    .abs().values
                spectral_values_1 = (pd.to_numeric(
                    row[1][:-3] * esl.light)) / 100  # the /100 because of the percentages
                spectral_values_2 = (esl.light * tau) / 100  # the /100 because of the percentages
                fi_lambda = fi_lambda.append(spectral_values_1.append(row[1][-3:]), ignore_index=True)
                fi_lambda.iloc[-1, -3] = 'Reflection'
                fi_lambda = fi_lambda.append(spectral_values_2.append(row[1][-3:]), ignore_index=True)
                fi_lambda.iloc[-1, -3] = 'Transmission'

            if e.args[0].find('SZ') >= 0:
                tau = pd.to_numeric(
                    tl.df.loc[tl.df['measurement number'] == row[1][-1]].loc[row[1][-3].replace('SZ', 'ZS')][:-1]) \
                    .abs().values

                # spectral_values = (pd.to_numeric(
                #     row[1][:-3] * esl.light) * tau) / 10000  # the /10000 because of the percentages
                # fi_lambda = fi_lambda.append(spectral_values.append(row[1][-3].replace('SZ', 'ZS')).append(row[1][-2:]),
                #                              ignore_index=True)

                spectral_values_1 = (pd.to_numeric(
                    row[1][:-3] * esl.light)) / 100  # the /100 because of the percentages
                spectral_values_2 = (esl.light * tau) / 100  # the /100 because of the percentages
                fi_lambda = fi_lambda.append(spectral_values_1.append(row[1][-3:].replace('SZ', 'ZS')),
                                             ignore_index=True)
                fi_lambda.iloc[-1, -3] = 'Reflection'
                fi_lambda = fi_lambda.append(spectral_values_2.append(row[1][-3:].replace('SZ', 'ZS')),
                                             ignore_index=True)
                fi_lambda.iloc[-1, -3] = 'Transmission'

        except KeyError as ee:
            print("you've ****** it up this time, a missing measurement:")
            print(ee)
        if e.args[0][0] != '5' or e.args[0][0] != 'H':
            pass
        else:
            raise e
fi_lambda.to_csv('data/results/fi_lambda.csv')
print('fi_lambda saved')

X_Y_Z_data = pd.DataFrame(columns=['X', 'Y', 'Z', 'x', 'y', 'z', 'Name', 'RT', 'Gloss', 'measurement number'])
for row in fi_lambda.iterrows():
    # numeric integrate: dx is always 5nm.. y=fi_lambda*x_overline
    append_me = pc.calculate_xyz(esl, row[1][:-4])
    append_me = append_me + list(row[1][-4:].values)
    X_Y_Z_data.loc[len(X_Y_Z_data)] = append_me
X_Y_Z_data.to_csv('data/results/X_Y_Z_data.csv')
print('X, Y, Z data saved')

faulty = 0  # it stores, how many records haven't passed the lightness test
L_a_b_data = pd.DataFrame(columns=['L', 'a', 'b', 'Name', 'RT', 'Gloss', 'measurement number'])
Xn, Yn, Zn = pc.calculate_xyz(esl, esl.light)[:3]
for row in X_Y_Z_data.iterrows():
    X, Y, Z = row[1][:3]
    if Y / Yn < 0.01 or X / Xn < 0.01 or Z / Zn < 0.01:
        faulty += 1
    L = 116 * (Y / Yn) ** (1 / 3) - 16
    a = 500 * ((X / Xn) ** (1 / 3) - (Y / Yn) ** (1 / 3))
    b = 200 * ((Y / Yn) ** (1 / 3) - (Z / Zn) ** (1 / 3))
    append_me = [L, a, b] + list(row[1][-4:].values)
    L_a_b_data.loc[len(L_a_b_data)] = append_me
print('faulty ones: ' + str(faulty) + ' of ' + str(L_a_b_data.shape[0]))
L_a_b_data.to_csv('data/results/L_a_b_data.csv')
print('L, a, b data saved')

names = set(L_a_b_data['Name'])
delta = []
for name in names:
    # hardcoded SCE Transmission
    mask = (L_a_b_data.Name == name) & (L_a_b_data.Gloss == 'SCE') & (L_a_b_data.RT == 'Transmission')
    delta_Lab = (L_a_b_data[mask].sort_values('measurement number')).iloc[:, 0:3].diff()[1:]
    diffs = list(delta_Lab.applymap(lambda x: x ** 2).sum(1).apply(np.sqrt))
    diffs.extend([name, 'SCE', 'Transmission'])
    delta.append(diffs)

    # hardcoded SCE Reflection
    mask = (L_a_b_data.Name == name) & (L_a_b_data.Gloss == 'SCE') & (L_a_b_data.RT == 'Reflection')
    delta_Lab = (L_a_b_data[mask].sort_values('measurement number')).iloc[:, 0:3].diff()[1:]
    diffs = list(delta_Lab.applymap(lambda x: x ** 2).sum(1).apply(np.sqrt))
    diffs.extend([name, 'SCE', 'Reflection'])
    delta.append(diffs)

    # hardcoded SCI Transmission
    mask = (L_a_b_data.Name == name) & (L_a_b_data.Gloss == 'SCI') & (L_a_b_data.RT == 'Transmission')
    delta_Lab = (L_a_b_data[mask].sort_values('measurement number')).iloc[:, 0:3].diff()[1:]
    diffs = list(delta_Lab.applymap(lambda x: x ** 2).sum(1).apply(np.sqrt))
    diffs.extend([name, 'SCI', 'Transmission'])
    delta.append(diffs)

    # hardcoded SCI Reflection
    mask = (L_a_b_data.Name == name) & (L_a_b_data.Gloss == 'SCI') & (L_a_b_data.RT == 'Reflection')
    delta_Lab = (L_a_b_data[mask].sort_values('measurement number')).iloc[:, 0:3].diff()[1:]
    diffs = list(delta_Lab.applymap(lambda x: x ** 2).sum(1).apply(np.sqrt))
    diffs.extend([name, 'SCI', 'Reflection'])
    delta.append(diffs)

final_final_delta_master_values_v3 = pd.DataFrame(delta)
final_final_delta_master_values_v3.to_csv('data/results/final_delta.csv')
print('final delta values saved')
tr = Transformer(L_a_b_data)
asd=6
