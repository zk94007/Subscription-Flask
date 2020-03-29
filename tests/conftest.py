import os
import pytest

from src import create_app
from src.models.base import db as db_instance
from src.models.subscriptions import Subscription
from src.models.service_codes import Plan, ServiceCode
from src.models.usages import DataUsage
from config import TestConfig

os.environ["FLASK_CONFIG"] = 'testing'


@pytest.yield_fixture(scope='session')
def app():
    app = create_app(TestConfig)

    with app.app_context():
        yield app


@pytest.fixture
def app_context(app):
    with app.app_context() as ctx:
        yield ctx


@pytest.fixture
def test_client(app, app_context):
    return app.test_client()


@pytest.yield_fixture(scope='session')
def db(app):
    with app.app_context():
        db_instance.drop_all()
        db_instance.create_all()
        db_instance.session.add(Plan(id=1,description="1GB Monthly Data Plan", mb_available=1024, is_unlimited=0))
        db_instance.session.add(Plan(id=2,description="5GB Monthly Data Plan", mb_available=5120, is_unlimited=0))
        db_instance.session.add(Plan(id=3,description="Unlimited Monthly Data Plan", mb_available=10240, is_unlimited=1))
        db_instance.session.add(ServiceCode(id=1, name="Data Block", description="Blocks all data"))
        db_instance.session.add(Subscription(phone_number="11111", status="active", plan_id="1"))
        db_instance.session.add(DataUsage(mb_used=1562, subscription_id=1))
        db_instance.session.commit()
        yield db_instance

@pytest.yield_fixture(scope="class", autouse=True)
def session(app, db, request):
    """
    Returns function-scoped session.
    """
    with app.app_context():
        conn = db_instance.engine.connect()
        txn = conn.begin()

        options = dict(bind=conn, binds={})
        sess = db_instance.create_scoped_session(options=options)

        db_instance.session = sess
        yield sess

        sess.remove()
        # This instruction rollsback any commit that were executed in the tests.
        txn.rollback()
