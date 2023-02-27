from app.db.models import Texts, Sentences, TokenizedTexts, Mistakes, Corrections
import os

DATABASE = os.environ["DATABASE"]
DB_USER = os.environ["POSTGRES_USER"]
DB_PASSWORD = os.environ["POSTGRES_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["POSTGRES_DB"]
DB_CONNECTION = f"{DATABASE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

FILES_PATH = "/code/data/Exam"
YEARS = [2014, 2015, 2016, 2017, 2019, 2020]
FILES_ORDER = ['text_table.tsv', 'new_sentence_text_table.tsv',
               'new_tokenized_text_table.tsv', 'mistakes_table.tsv', 'tokenized_corrections_table.tsv']
TABLES_ORDER = [Texts, Sentences, TokenizedTexts, Mistakes, Corrections]
