from constants import Building, File
from datetime import datetime
from pathlib import Path
from os import listdir
from os.path import isfile, join


def extract_department_and_building(string):
    building = Building.A15
    dept = string

    # extract building
    if Building.A2 in string:
        building = Building.A2
    elif Building.A14 in string:
        building = Building.A14

    # extract dept
    dept = dept.replace(building, '').rstrip()

    return dept, building


def form_output_file(file_dir):
    now = datetime.now().strftime('%d-%m-%Y %H-%M-%S')
    file_name = File.OUTPUT_FILE + now + ".xlsx"
    return Path(file_dir) / file_name


def files_in_dir(directory):
    return [join(directory, f) for f in listdir(directory) if isfile(join(directory, f))]
