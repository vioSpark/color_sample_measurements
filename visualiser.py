"""
Konzi Ágival:
TDK leshet belőle
L_a_b koordinátákra egy átlag, és +- szórás
0.01-es errort megnézni

színminták közti delta E-k et számolni, és vizualizálni (pl 1-estől mennyire különbözik a 2-es, attól mennyire a 3-as ,stb.....)
Ezt megnézni Márk 1. mintájára --> alapból jó volt-e a mérés
Ennek az átlagát, és szórását nézni, és így lehet összehasonlítani a különböző színeket

Prezibe ezt, meg ennek a változását lehet rakni, h result is legyen
optional: Chroma (a) + hue (b) -> mennyire változott (párolgás miatt a L-t nem nézni)

ppt-t átdobhatjuk megnézésre (pár napos delay)

"""

import numpy as np
import logging
import datetime as dt
import sys
import pandas as pd
import scipy as sc


class Transformer:
    def __init__(self, L_a_b_data):
        columns = list(L_a_b_data.columns.values) + ['Temperature', 'Water type', 'Color', 'Shade ID']
        tmp = pd.concat([L_a_b_data, L_a_b_data.Name.str[:1], L_a_b_data.Name.str[1:2], L_a_b_data.Name.str[2:3],
                         pd.DataFrame(np.nan, index=range(len(L_a_b_data)), columns=['A'])], axis=1)
        tmp.columns = columns
        # get the Shade ID-s fixed ... I have no ide why have I calculated this....
        tmp.update(pd.to_numeric(tmp[tmp['Color'] == 'P'].loc[:, 'Name'].str[3:].rename('Shade ID')))
        tmp.update(pd.to_numeric(tmp[tmp['Color'] == 'Z'].loc[:, 'Name'].str[4:].rename('Shade ID')))
        tmp.sort_values(by=['RT', 'Gloss', 'Color', 'Water type', 'Temperature', 'measurement number', 'Shade ID'],
                        inplace=True)

        final = pd.DataFrame(
            columns=['1->2', '2->3', '3->4', '4->5', '5->6', '6->7', '7->8', '8->9', '9->10', '10->11', 'RT',
                     'Gloss', 'Color', 'Water type', 'Temperature', 'measurement number'])
        measurements = tmp.loc[:, 'measurement number'].max()
        gloss_type = ('SCI', 'SCE')
        rt_type = ('Transmission', 'Reflection')
        temp_type = ('5', 'H')
        water_type = ('+', 'D', 'M')
        color_type = ('P', 'Z')
        index = 0
        for gloss in range(2):
            for rt in range(2):
                for temp in range(2):
                    for water in range(3):
                        for color in range(2):
                            for meas_num in range(measurements + 1):
                                mask = (tmp.Gloss == gloss_type[gloss]) & \
                                       (tmp.RT == rt_type[rt]) & \
                                       (tmp.loc[:, 'Temperature'] == temp_type[temp]) & \
                                       (tmp.loc[:, 'Water type'] == water_type[water]) & \
                                       (tmp.loc[:, 'Color'] == color_type[color]) & \
                                       (tmp.loc[:, 'measurement number'] == meas_num)
                                res = tmp.loc[mask]
                                # name = res.loc['Name']
                                delta_Lab = res.loc[:, 'L':'b'].diff().iloc[1:]
                                diffs = list(delta_Lab.applymap(lambda x: x ** 2).sum(1).apply(np.sqrt))
                                try:
                                    final.loc[index] = diffs + [rt_type[rt], gloss_type[gloss], color_type[color],
                                                                water_type[water], temp_type[temp], meas_num]

                                except ValueError as e:
                                    print(str(meas_num) + ' ' + str(temp_type[temp]) + str(water_type[water]) + str(
                                        color_type[color]) + ' ' + str(rt_type[rt]) + ' ' + str(gloss_type[gloss]))
                                index += 1
        """
        method for one:
        mask = (tmp.Gloss == 'SCI') & (tmp.RT == 'Reflection') & (tmp['measurement number'] == 0) & (
                tmp['Temperature'] == '5') & (tmp['Water type'] == 'D') & (tmp['Color'] == 'P')
        res = tmp.loc[mask]
        delta_Lab = res.loc[:, 'L':'b']
        diffs = list(delta_Lab.applymap(lambda x: x ** 2).sum(1).apply(np.sqrt))
        """
        avg, std = final.iloc[:10].mean(axis=1, numeric_only=True).rename('average'), \
                   final.iloc[:10].std(axis=1, numeric_only=True).rename(
                       'standard deviation')
        final = pd.concat([final, avg, std], axis=1, join_axes=[final.index])
        final.to_csv('data/results/final_final.csv')
        print('final_final.csv saved')
