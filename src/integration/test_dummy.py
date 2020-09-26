import pytest, time, logging

from modules.pytg.development import add_reroute_rule
from modules.pytg.load import manager

from modules.pytg.testing.utils.triggers.success import SuccessGuard

from dev_modules.dummy_tests.integration.utils import setup_environment, teardown_environment, load_test_update, load_test_yaml, load_test_json

@pytest.fixture(autouse=True)
def test_container():
    setup_environment()
    yield
    teardown_environment()

def test_dummy():
    assert True