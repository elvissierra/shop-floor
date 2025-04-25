import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.models import Base
from controller import MutationService, QueryService
from schema import DepartmentInput

@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    sess = TestingSessionLocal()
    yield sess
    sess.close()

def test_add_and_get_department(session):
    service = MutationService(session)
    input_data = DepartmentInput(title="D1", description="Desc1")
    dept = service.add_department(input_data)

    assert dept.id is not None
    assert dept.title == "D1"
    assert dept.description == "Desc1"

    qservice = QueryService(session)
    all_depts = qservice.get_all_departments()
    assert len(all_depts) == 1
    assert all_depts[0].title == "D1"
