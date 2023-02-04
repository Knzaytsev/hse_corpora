from app.api.constants import WORDS_COLUMNS, POSTFIX_PATTERN, MODEL_FIELDS, NUM_FIELDS
from app.api.search_module.search_engine import exec_search


def filter_fields(row):
    output = dict()
    for field in MODEL_FIELDS:
        if field in row:
            output[field] = row[field]
    return output

def controller_exec_search(forms):
    result = exec_search(forms)

    for row in result:
        for column in WORDS_COLUMNS:
            column_vals = []
            offset = 0
            for i, form in enumerate(forms):
                if form['by'] in ['mistake']:
                    offset += 1
                    continue
                column_vals.append(row.pop(column + POSTFIX_PATTERN(i - offset)))
            row[column] = column_vals

        row[NUM_FIELDS] = len(forms)

    result = [filter_fields(row) for row in result]

    return result
