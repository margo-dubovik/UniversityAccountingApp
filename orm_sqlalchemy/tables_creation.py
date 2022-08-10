from sqlalchemy import create_engine
from models import Base

engine = create_engine('postgresql+psycopg2://postgres:default@localhost:5432/university_db', echo=True)

Base.metadata.create_all(engine)