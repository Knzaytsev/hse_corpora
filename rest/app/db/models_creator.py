from app.db.models import Texts, Sentences, TokenizedTexts, Mistakes, Corrections
from app.db.utils import create_table, import_data
from app.db.settings import YEARS, FILES_ORDER, TABLES_ORDER, FILES_PATH
from os import listdir
from os.path import isfile, join
import re


def create_tables():
    tables = [Texts, Sentences, TokenizedTexts, Mistakes, Corrections]
    error = ""
    try:
        for table in tables:
            create_table(table.metadata)
    except Exception as e:
        error = str(e)
    return error


def fulfill_tables():
    try:
        for year in YEARS:
            file_path = FILES_PATH + str(year)
            year_prefix = str(year) + '_'
            tasks = listdir(file_path)
            for task in tasks:
                files = [f for f in listdir(join(file_path, task)) if isfile(join(file_path, task, f))]
                if sum([year_prefix + ordered_file in file
                        for ordered_file in FILES_ORDER
                        for file in files]) != len(FILES_ORDER):
                    raise Exception(str(files))
                paths = []
                for oredered_file in FILES_ORDER:
                    for file in files:
                        if year_prefix + oredered_file in file:
                            paths.append(join(file_path, task, file))
                            break
                    files.remove(file)
                task_id = int(re.findall(r'\d+', task)[0])
                error = import_data(paths, TABLES_ORDER, year, task_id)
                if error:
                    raise Exception(error)
    except Exception as e:
        error = str(e)

    return error
