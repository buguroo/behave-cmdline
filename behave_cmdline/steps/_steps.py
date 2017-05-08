from functools import partial
import re

from .process import Process


def i_set_the_following_environment_variables(context):
    """
    Update `context.env` with the values of the table:

    - Column `name`: Variable name.
    - Column `value`: Variable value.

    """
    for row in context.table:
        context.cmdline_env[row["name"]] = row["value"]


def i_run_this_command(context, alias="default"):
    """
    Run the command and wait for it to end.

    If the comand exists with a return code other than 0 an exception
    will be raised.

    """
    process = Process(context.text, context.cmdline_env, daemon=False)

    context.cmdline_processes[alias] = process
    context.cmdline_exitstack.enter_context(process)


def i_launch_this_daemon(context, alias="default"):
    """
    Launch a long running process.

    """
    process = Process(context.text, context.cmdline_env, daemon=True)

    context.cmdline_processes[alias] = process
    context.cmdline_exitstack.enter_context(process)


def i_see_in_the_output_of(context, stream, alias="default", timeout=None):
    """

    Search on the output `stream` of the `alias` command looking for the
    table values.

        - Column `mode`: `plain`/`regex`
        - Column `shows`: `Y`/`N`
        - Column `value`: The text or regex to match or not.

    """
    def plain_matcher(fragment, line):
        return fragment in line

    def regex_matcher(regex, line):
        return re.match(regex, line)

    checks = []
    for row in context.table:

        if row["shows"] == "Y":
            shows = True
        elif row["shows"] == "N":
            shows = False
        else:
            raise ValueError("Unknown value for column `shows`")

        if row["mode"] == "plain":
            do_match = partial(plain_matcher, row["value"])
        elif row["mode"] == "regex":
            do_match = partial(regex_matcher, row["value"])
        else:
            raise ValueError("Unknown value for column `mode`")

        def check_lines():
            try:
                while True:
                    if do_match((yield)):
                        if not shows:
                            assert False, row
                        else:
                            return
            except GeneratorExit as exc:
                if shows:
                    assert False, row

        check = check_lines()
        check.send(None)
        checks.append(check)

    context.cmdline_processes[alias].check_stream(
        stream, *checks, timeout=timeout)
