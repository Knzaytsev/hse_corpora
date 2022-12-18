from app.db.models import Texts, Sentences, TokenizedTexts, Mistakes, Corrections
from app.db.db_utils import create_table, import_data

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
    tables = [Texts, Sentences, TokenizedTexts, Mistakes, Corrections]
    paths = [
        "/code/data/Exam2020/Exam2020_Task_1_Essays_1_918_text_table.tsv", 
        "/code/data/Exam2020/Exam2020_Task_1_Essays_1_918_new_sentence_text_table.tsv",
        "/code/data/Exam2020/Exam2020_Task_1_Essays_1_918_new_tokenized_text_table.tsv",
        "/code/data/Exam2020/Exam2020_Task_1_Essays_1_918_mistakes_table.tsv",
        "/code/data/Exam2020/Exam2020_Task_1_Essays_1_918_tokenized_corrections_table.tsv"
             ]
    error = import_data(paths, tables)
    return error