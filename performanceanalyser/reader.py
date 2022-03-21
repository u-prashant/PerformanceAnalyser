import pandas as pd
from constants import Column, Sheet


class Reader:
    @staticmethod
    def read_config_file(file):
        print('Reading {} file'.format(file))
        xls = pd.ExcelFile(file)
        count_data_columns = pd.read_excel(xls, Sheet.COUNT_DATA_COLUMNS_CONFIG)[Column.COLUMNS].tolist()
        time_data_columns = pd.read_excel(xls, Sheet.TIME_DATA_COLUMNS_CONFIG)[Column.COLUMNS].tolist()
        count_data_op_sequence = pd.read_excel(xls, Sheet.COUNT_DATA_OUTPUT_SEQUENCE_CONFIG)[Column.COLUMNS].tolist()
        time_data_op_sequence = pd.read_excel(xls, Sheet.TIME_DATA_OUTPUT_SEQUENCE_CONFIG)[Column.COLUMNS].tolist()
        tat_df = pd.read_excel(xls, Sheet.TAT_CONFIG).fillna(0)
        tat = dict(zip(tat_df[Column.DEPARTMENT], tat_df[Column.TAT]))
        return count_data_columns, time_data_columns, count_data_op_sequence, time_data_op_sequence, tat

    @staticmethod
    def read_raw_files(files):
        count_dfs = []
        time_dfs = []
        for file in files:
            print('Reading {} file'.format(file))
            xls = pd.ExcelFile(file)

            # Read & Clean Count DF
            count_df = pd.read_excel(xls, Sheet.COUNT_DATA)
            count_df = count_df[:len(count_df)-2]
            count_dfs.append(count_df)

            # Read Time DF
            time_df = pd.read_excel(xls, Sheet.TIME_DATA)
            time_dfs.append(time_df)

        return pd.concat(count_dfs), pd.concat(time_dfs)
