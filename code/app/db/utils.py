import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from psycopg2.extensions import register_adapter, AsIs
from app.db.settings import DB_CONNECTION

register_adapter(np.float64, lambda x: AsIs(x))
register_adapter(np.int64, lambda x: AsIs(x))

engine = create_engine(DB_CONNECTION)

def exec_statement(stmt):
    result = None
    with Session(engine) as session:
        result = session.execute(stmt)
        result = [row for row in result]
    return result
    

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
    data = pd.read_csv(file_name, delimiter='\t', encoding='utf-16')
    data = data.where(data.notna(), None)
    return data

def create_table(metadata):
    metadata.create_all(engine)

def import_data(file_names, tables, year):
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

    error = ""
    try:
        for file_name, table in zip(file_names, tables):
            data = load_data(file_name)
            data['text_year'] = year
            headers = data.columns
            headers = [column for column in dir(table) if column in headers]
            for i in range(len(data)):
                row = data.iloc[i]
                mapped_cols = {col: None if pd.isna(row[col]) else row[col] for col in headers}
                record = table(**mapped_cols)
                s.add(record)
                if i % 100 == 0:
                    s.commit()
            s.commit()
    except Exception as e:
        s.rollback()
        error = str(year) + " " + str(e)
    finally:
        s.close()
    return error