class APP:
    NAME = '''
    ONE CLICK SOLUTION
    
        TAT Report
    '''
    TITLE = ''
    SOURCE_STATIC_LABEL = 'Raw Files'
    TARGET_STATIC_LABEL = 'Destination Folder'
    SELECT_RAW_FILES = 'Select Raw Files'
    SELECT_DESTINATION_FOLDER = 'Select Destination Folder'
    NO_FILES_SELECTED = 'No Files Selected'
    NO_DIR_SELECTED = 'No Directory Selected'
    BROWSE = 'Browse'
    EXIT = 'Exit'
    GENERATE_REPORT = 'Generate Report'


class Colors:
    AZURE3 = 'azure3'
    AZURE4 = 'azure4'
    BLUE = 'blue'
    WHITE = 'white'
    GRAY25 = 'gray25'
    NAVY = 'navy'


class File:
    CONFIG_FILE = r'data/ConfigData.xlsx'
    OUTPUT_FILE = 'PerformanceSummary_'
    CONFIG_PICKLE_FILE = r'data/config.pkl'


class FilesKey:
    OUTPUT_FILE = 1
    INPUT_FILES = 2


class Column:
    COLUMNS = 'Columns'
    TAT = 'TAT'

    STOCK = 'Stock'

    DEPARTMENT = 'Department'
    BUILDING = 'Building'
    TOTAL = 'Total Count'

    ONE_TIME = '1 Time'
    TWO_TIMES = '2 Times'
    MORE_THAN_TWO_TIMES = '2+ Times'
    TOTAL_COUNT = '[Total Count]'
    ONE_TIME_PERCENT = 'One Time (%age)'
    TWO_TIMES_PERCENT = 'Two Times (%age)'
    MORE_THAN_TWO_TIMES_PERCENT = 'Two Times Plus (%age)'

    PERCENTILE_50 = '50 Percentile (in mins)'
    PERCENTILE_75 = '75 Percentile (in mins)'
    PERCENTILE_95 = '95 Percentile (in mins)'
    STD_DEVIATION = 'Standard Deviation (in mins)'

    PERCENT = 'Orders processed within TAT (%age)'

    DS_A2 = 'DS A2'
    DS_A14 = 'DS A14'
    DS_A15 = 'DS_A15'
    TS_A14 = 'TS A14'
    TS_A15 = 'TS A15'
    DS_Rework_A2 = 'DS - rework A2'
    DS_Rework_A14 = 'DS - rework A14'
    DS_Rework_A15 = 'DS - rework A15'
    TS_Rework_A14 = 'TS - rework A14'
    TS_Rework_A15 = 'TS - rework A15'
    LW = 'LW'
    Inventory = 'Inventory'


class Sheet:
    COUNT_DATA = 'count_data'
    TIME_DATA = 'time_data'
    TAT_DATA = 'tat_data'

    COUNT_DATA_COLUMNS_CONFIG = 'CountDataColumns'
    TIME_DATA_COLUMNS_CONFIG = 'TimeDataColumns'
    COUNT_DATA_OUTPUT_SEQUENCE_CONFIG = 'CountDataOutputSequence'
    TIME_DATA_OUTPUT_SEQUENCE_CONFIG = 'TimeDataOutputSequence'
    TAT_CONFIG = 'TAT'


class Building:
    A2 = 'A2'
    A14 = 'A14'
    A15 = 'A15'


class Processed:
    ZERO_TIME = 0
    ONE_TIME = 1
    TWO_TIMES = 2


class Percentile:
    FIFTY = 0.50
    SEVENTY_FIVE = 0.75
    NINETY_FIVE = 0.95


class Error:
    INPUT_FILES_NOT_PROVIDED = 'ERROR: Input files are not provided !!!'
    OUTPUT_FILE_NOT_PROVIDED = 'ERROR: Output file path not provided !!!'
    CONFIG_NOT_FOUND = 'ERROR: Config not found !!!'

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

