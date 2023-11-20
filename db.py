from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import os


Base = declarative_base()

load_dotenv()

db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_engine = os.getenv("DB_ENGINE")

if db_engine == "mysql":
    db_url = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}"
elif db_engine == "sqlite":
    db_url = f"sqlite:///{db_name}"
elif db_engine == "postgresql":
    db_url = f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}"
elif db_engine == "test":
    # db_url = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}/testdb"
    db_url = "sqlite:///test.db"

engine = create_engine(db_url)

session_maker = sessionmaker(bind=engine)

DB_RECORD_NOT_FOUND = "Record not Found"
DB_TEAM_NOT_EMPTY = "The team is not empty"
