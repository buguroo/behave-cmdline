import pytest
from argparse import Namespace
from behave_cmdline import environment as env


@pytest.fixture(scope="function")
def dummy_context():
    ns = Namespace()
    env.before_scenario(ns, None)
    yield ns
    env.after_scenario(ns, None)
