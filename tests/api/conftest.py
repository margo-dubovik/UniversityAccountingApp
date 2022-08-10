import pytest

from flask_sqlalchemy import SQLAlchemy

import university_accounting_api



@pytest.fixture(scope='session')
def client():
    db_uri = "postgresql+psycopg2://postgres:default@localhost:5432/test_university_db"
    university_accounting_api.app.config['TESTING'] = True
    university_accounting_api.app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    client = university_accounting_api.app.test_client()
    yield client