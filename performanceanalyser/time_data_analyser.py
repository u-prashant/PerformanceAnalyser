from analyser import Analyser
from constants import Sheet, Column, Percentile
from utils import extract_department_and_building
from pandas.api.types import is_numeric_dtype

import pandas as pd
import numpy as np


class TimeDataAnalyser(Analyser):
    def __init__(self, workbook, df, columns, output_seq):
        self.workbook = workbook
        self.df = df
        self.departments_to_process = columns
        self.output_seq = output_seq

    def name(self):
        return 'Time Data Analyser'

    @staticmethod
    def get_sheet():
        return Sheet.TIME_DATA

    def analyse(self):
        total_df = self.df
        stock_df = self.df[self.df[Column.STOCK] == 'Stock']
        rx_df = self.df[self.df[Column.STOCK] != 'Stock']

        self.get_pivot(total_df, 'total')
        self.get_pivot(rx_df, 'rx')
        self.get_pivot(stock_df, 'stock')

    def get_pivot(self, df, name):
        count_stat_df = self.compute_time_stat(df)
        pivot = self.pivot_time_stat(count_stat_df)
        pivot.to_excel(self.workbook, sheet_name=self.get_sheet() + '_' + name)

    def pivot_time_stat(self, df):
        values = [
            Column.PERCENTILE_50,
            Column.PERCENTILE_75,
            Column.PERCENTILE_95,
            Column.STD_DEVIATION,
            Column.TOTAL_COUNT
        ]
        rows = [Column.DEPARTMENT]
        columns = [Column.BUILDING]
        df[Column.DEPARTMENT] = df[Column.DEPARTMENT].astype(pd.api.types.CategoricalDtype(self.output_seq, ordered=True))
        pivot = pd.pivot_table(df, values=values, index=rows, columns=columns, aggfunc=np.sum, fill_value=0)
        return pivot.replace(0, '')

    def compute_time_stat(self, df):
        time_info = []

        for column in self.departments_to_process:
            dept, building = extract_department_and_building(column)

            if not is_numeric_dtype(df[column]):
                print('Ignoring {} Column as it is not a numeric column'.format(column))
                continue

            # compute percentile time, std
            std = round(df[df[column] != 0][column].std(), 0)
            total = len(df[df[column] != 0])
            percentiles = df[df[column] != 0][column].quantile([.5, .75, .95])
            percentile_50, percentile_75, percentile_95 = 0, 0, 0
            for percentile, percentile_value in percentiles.items():
                if percentile == Percentile.FIFTY:
                    percentile_50 = round(percentile_value, 0)
                elif percentile == Percentile.SEVENTY_FIVE:
                    percentile_75 = round(percentile_value, 0)
                elif percentile == Percentile.NINETY_FIVE:
                    percentile_95 = round(percentile_value, 0)

            time_info.append([dept, building, percentile_50, percentile_75, percentile_95, std, total])

        time_stat_df_columns = [
            Column.DEPARTMENT,
            Column.BUILDING,
            Column.PERCENTILE_50,
            Column.PERCENTILE_75,
            Column.PERCENTILE_95,
            Column.STD_DEVIATION,
            Column.TOTAL_COUNT
        ]
        return pd.DataFrame(time_info, columns=time_stat_df_columns)
