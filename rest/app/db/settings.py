from app.db.models import Texts, Sentences, TokenizedTexts, Mistakes, Corrections

DATABASE = "postgresql"
DB_USER = "corpora_user"
DB_PASSWORD = "corpora_user"
DB_HOST = "postgres_container"
DB_PORT = 5432
DB_NAME = "corpora_db"
DB_CONNECTION = f"{DATABASE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

FILES_PATH = "/code/data/Exam"
YEARS = [2014, 2015, 2016, 2017, 2019, 2020]
FILES_ORDER = ['text_table.tsv', 'new_sentence_text_table.tsv',
               'new_tokenized_text_table.tsv', 'mistakes_table.tsv', 'tokenized_corrections_table.tsv']
TABLES_ORDER = [Texts, Sentences, TokenizedTexts, Mistakes, Corrections]
