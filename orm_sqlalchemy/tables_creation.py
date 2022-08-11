from sqlalchemy import create_engine
from models import Base
from dotenv import load_dotenv
import os

load_dotenv()


engine = create_engine("postgresql+psycopg2://{}:{}@{}:{}/{}".format(
            os.environ.get('DB_USERNAME'),
            os.environ.get('DB_PASSWORD'),
            os.environ.get('DB_HOST'),
            os.environ.get('DB_PORT'),
            os.environ.get('DB_NAME'),
        ), echo=True)

Base.metadata.create_all(engine)