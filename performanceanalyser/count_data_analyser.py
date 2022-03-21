from analyser import Analyser
from constants import Sheet, Processed, Column
from utils import extract_department_and_building
from pandas.api.types import is_numeric_dtype

import pandas as pd
import numpy as np


class CountDataAnalyser(Analyser):
    def __init__(self, workbook, df, columns, output_seq):
        self.workbook = workbook
        self.df = df
        self.departments_to_process = columns
        self.output_seq = output_seq

    def name(self):
        return 'Count Data Analyser'

    @staticmethod
    def get_sheet():
        return Sheet.COUNT_DATA

    def analyse(self):
        total_df = self.df
        stock_df = self.df[self.df[Column.STOCK] == 'Stock']
        rx_df = self.df[self.df[Column.STOCK] != 'Stock']

        self.get_pivot(total_df, 'total')
        self.get_pivot(rx_df, 'rx')
        self.get_pivot(stock_df, 'stock')

    def get_pivot(self, df, name):
        count_stat_df = self.compute_count_stat(df)
        pivot = self.pivot_count_stat(count_stat_df)
        pivot.to_excel(self.workbook, sheet_name=self.get_sheet() + '_' + name)

    def pivot_count_stat(self, df):
        values = [
            Column.ONE_TIME,
            Column.TWO_TIMES,
            Column.MORE_THAN_TWO_TIMES,
            Column.ONE_TIME_PERCENT,
            Column.TWO_TIMES_PERCENT,
            Column.MORE_THAN_TWO_TIMES_PERCENT,
            Column.TOTAL_COUNT
        ]
        rows = [Column.DEPARTMENT]
        columns = [Column.BUILDING]
        df[Column.DEPARTMENT] = df[Column.DEPARTMENT].astype(pd.api.types.CategoricalDtype(self.output_seq, ordered=True))
        pivot = pd.pivot_table(df, values=values, index=rows, columns=columns, aggfunc=np.sum, fill_value=0)
        return pivot.replace(0, '')

    def compute_count_stat(self, df):
        count_info = []

        for column in self.departments_to_process:
            dept, building = extract_department_and_building(column)

            if not is_numeric_dtype(df[column]):
                print('Ignoring {} Column as it is not a numeric column'.format(column))
                continue

            # compute counts for single, twice and more than twice processing
            value_counts = df[column].value_counts()
            one_time, two_times, more_than_two_times = 0, 0, 0
            one_time_percent, two_times_percent, more_than_two_times_percent = 0, 0, 0
            for times, count in value_counts.items():
                if times == Processed.ONE_TIME:
                    one_time = count
                elif times == Processed.TWO_TIMES:
                    two_times = count
                elif times != Processed.ZERO_TIME:
                    more_than_two_times += count

            total_count = one_time + two_times + more_than_two_times
            if total_count != 0:
                one_time_percent = round((one_time * 100) / total_count, 1)
                two_times_percent = round((two_times * 100) / total_count, 1)
                more_than_two_times_percent = round((more_than_two_times * 100) / total_count, 1)

            count_info.append([dept, building, one_time, two_times, more_than_two_times, one_time_percent,
                               two_times_percent, more_than_two_times_percent, total_count])

        count_stat_df_columns = [
            Column.DEPARTMENT,
            Column.BUILDING,
            Column.ONE_TIME,
            Column.TWO_TIMES,
            Column.MORE_THAN_TWO_TIMES,
            Column.ONE_TIME_PERCENT,
            Column.TWO_TIMES_PERCENT,
            Column.MORE_THAN_TWO_TIMES_PERCENT,
            Column.TOTAL_COUNT
        ]
        return pd.DataFrame(count_info, columns=count_stat_df_columns)
