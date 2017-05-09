from collections import defaultdict
from contextlib import ExitStack
import os


def before_scenario(context, scenario):
    context.cmdline_env = dict(os.environ)
    context.cmdline_processes = defaultdict(list)
    context.cmdline_exitstack = ExitStack().__enter__()


def after_scenario(context, scenario):
    context.cmdline_exitstack.close()
