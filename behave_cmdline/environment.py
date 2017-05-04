def before_scenario(context, scenario):
    context.cmdline_env = dict(os.environ)
    context.cmdline_processes = dict()
    context.cmdline_exitstack = ExitStack().__enter__()


def after_scenario(context, scenario):
    context.cmdline_exitstack.close()
