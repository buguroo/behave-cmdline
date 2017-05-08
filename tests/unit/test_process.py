from datetime import datetime
from datetime import timedelta
import pytest


def test_daemon_process_context_manager():
    from behave_cmdline.steps.process import Process

    with Process("sleep 10", env={}, daemon=True) as p:
        assert p.process.returncode is None
    assert p.process.returncode is not None


def test_nondaemon_process_context_manager():
    from behave_cmdline.steps.process import Process

    start = datetime.now() 
    with Process("sleep 2", env={}) as p:
        inside = datetime.now()
    assert inside - start >= timedelta(seconds=2)


def test_process_environment_access():
    from behave_cmdline.steps.process import Process

    with Process("echo -n $MYVAR", env={'MYVAR': 'test'}) as p:
        pass

    assert b'test' == p.stdout_file.getvalue()
