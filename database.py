from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

from dotenv import load_dotenv
import os
load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")


db_engine =create_engine(DATABASE_URL)
local_session=sessionmaker(bind=db_engine,autoflush=False)
base=declarative_base()