from app.api.constants import MULTIPLE_COLUMNS, POSTFIX_PATTERN, MODEL_FIELDS, NUM_FIELDS
from app.api.search_engine import exec_search


def filter_fields(row):
    output = dict()
    for field in MODEL_FIELDS:
        output[field] = row[field]
    return output

def controller_exec_search(forms):
    result = exec_search(forms)

    for row in result:
        for column in MULTIPLE_COLUMNS:
            column_vals = []
            for i in range(len(forms)):
                column_vals.append(row.pop(column + POSTFIX_PATTERN(i)))
            row[column] = column_vals
        row[NUM_FIELDS] = len(forms)
    
    result = [filter_fields(row) for row in result]

    return result
