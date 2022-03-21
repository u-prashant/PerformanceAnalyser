from analyser import Analyser
from constants import Sheet, Column, Percentile
from utils import extract_department_and_building
from pandas.api.types import is_numeric_dtype

import pandas as pd
import numpy as np


class TATAnalyser(Analyser):
    TICK = '_'

    def __init__(self, workbook, df, columns, output_seq, tat):
        self.workbook = workbook
        self.df = df
        self.departments_to_process = columns
        self.output_seq = output_seq
        self.tat = tat

    def name(self):
        return 'TAT Data Analyser'

    @staticmethod
    def get_sheet():
        return Sheet.TAT_DATA

    def analyse(self):
        total_df = self.df
        stock_df = self.df[self.df[Column.STOCK] == 'Stock']
        rx_df = self.df[self.df[Column.STOCK] != 'Stock']

        self.get_pivot(total_df, 'total')
        self.get_pivot(rx_df, 'rx')
        self.get_pivot(stock_df, 'stock')

    def get_pivot(self, df, name):
        count_stat_df = self.compute_tat_stat(df)
        pivot = self.pivot_tat_stat(count_stat_df)
        pivot.to_excel(self.workbook, sheet_name=self.get_sheet() + '_' + name)

    def pivot_tat_stat(self, df):
        values = [Column.PERCENT]
        rows = [Column.DEPARTMENT]
        columns = [Column.BUILDING]
        df[Column.DEPARTMENT] = df[Column.DEPARTMENT].astype(pd.api.types.CategoricalDtype(self.output_seq, ordered=True))
        pivot = pd.pivot_table(df, values=values, index=rows, columns=columns, aggfunc=np.sum, fill_value=0)
        return pivot.replace(0, '')

    def compute_tat_stat(self, df):
        time_info = []

        for column in self.departments_to_process:
            dept, building = extract_department_and_building(column)

            if not is_numeric_dtype(df[column]):
                print('Ignoring {} Column as it is not a numeric column'.format(column))
                continue

            tat = 0
            if dept in self.tat:
                tat = self.tat.get(dept)

            # compute percent of requests completed within time
            total = len(df.loc[df[column] != 0])
            orders_within_tat = len(df.loc[(df[column] <= tat) & (df[column] != 0)])
            percent = 0
            if total != 0:
                percent = round((orders_within_tat * 100) / total, 0)

            time_info.append([dept, building, percent])

        time_stat_df_columns = [
            Column.DEPARTMENT,
            Column.BUILDING,
            Column.PERCENT
        ]
        return pd.DataFrame(time_info, columns=time_stat_df_columns)
