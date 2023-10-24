from sqlalchemy import create_engine
import pytest


@pytest.fixture()
def engine():
    db_url = "sqlite:///unit_test.db"
    engine = create_engine(db_url)
    yield engine
