DATABASE = "postgresql"
DB_USER = "corpora_user"
DB_PASSWORD = "corpora_user"
DB_HOST = "postgres_container"
DB_PORT = 5432
DB_NAME = "corpora_db"
DB_CONNECTION = f"{DATABASE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"