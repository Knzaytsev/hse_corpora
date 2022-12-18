import pandas as pd
import numpy as np
from time import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from psycopg2.extensions import register_adapter, AsIs
from app.db.settings import DB_CONNECTION
import sys

def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)
def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)
register_adapter(np.float64, lambda x: AsIs(x))
register_adapter(np.int64, lambda x: AsIs(x))

engine = create_engine(DB_CONNECTION)

def check_db_status():
    message = ""
    try:
        with engine.connect() as connection:
            result = connection.execute("select version()")
        message = result.fetchall()
    except Exception as e:
        message = str(e)
    return message

def load_data(file_name):
    data = pd.read_csv(file_name, delimiter='\t', encoding='utf-8')
    data = data.where(data.notna(), None)
    return data.columns, data

def create_table(metadata):
    metadata.create_all(engine)

def import_data(file_names, tables):
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

    error = ""
    try:
        for file_name, table in zip(file_names, tables):
            headers, data = load_data(file_name)
            headers = [column for column in dir(table) if column in headers]
            sys.stdout.writelines([file_name])
            for i in range(len(data)):
                row = data.iloc[i]
                mapped_cols = {col: None if pd.isna(row[col]) else row[col] for col in headers}
                record = table(**mapped_cols)
                s.add(record)
                if i % 100 == 0:
                    s.commit()
            s.commit()
    except Exception as e:
        error = str(e)
        s.rollback()
    finally:
        s.close()
    return error