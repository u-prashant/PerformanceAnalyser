from reader import Reader
from constants import File, FilesKey, Error
from count_data_analyser import CountDataAnalyser
from time_data_analyser import TimeDataAnalyser
from tat_analyser import TATAnalyser
from utils import form_output_file, files_in_dir
from preprocess import Preprocess

import pandas as pd


class Manager:
    @staticmethod
    def manage(files: dict):
        try:
            Manager.validate_files(files)
        except Exception as e:
            print(e)
            raise e

        count_df, time_df = Reader.read_raw_files(files.get(FilesKey.INPUT_FILES))
        count_data_columns, time_data_columns, count_data_op_sequence, time_data_op_sequence, tat = \
            Reader.read_config_file(File.CONFIG_FILE)

        count_df = Preprocess.preprocess(count_df)
        time_df = Preprocess.preprocess(time_df)

        workbook = pd.ExcelWriter(form_output_file(files.get(FilesKey.OUTPUT_FILE)), engine='xlsxwriter')

        analysers = [
            CountDataAnalyser(workbook, count_df, count_data_columns, count_data_op_sequence),
            TimeDataAnalyser(workbook, time_df, time_data_columns, time_data_op_sequence),
            TATAnalyser(workbook, time_df, time_data_columns, time_data_op_sequence, tat)
        ]

        for analyser in analysers:
            print('Running {} ...'.format(analyser.name()))
            analyser.analyse()

        workbook.save()
        print('Successfully Analysed the files !!!')

    @staticmethod
    def validate_files(files: dict):
        if FilesKey.INPUT_FILES not in files:
            raise Exception(Error.INPUT_FILES_NOT_PROVIDED)

        if FilesKey.OUTPUT_FILE not in files:
            raise Exception(Error.OUTPUT_FILE_NOT_PROVIDED)


if __name__ == '__main__':
    directory = r"C:/Users/grglogistic9/Desktop/TAT Output/Feb'22 TAT Output"
    files_list = files_in_dir(directory)
    # files_list = [
    #     r'tmp/2502.xlsx'
    # ]
    files_dict = {
        FilesKey.INPUT_FILES: files_list,
        FilesKey.OUTPUT_FILE: r'tmp'
    }
    Manager.manage(files_dict)
