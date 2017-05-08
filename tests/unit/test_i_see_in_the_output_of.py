import pytest

from behave.model import Table


#
# PLAIN MODE
#
def test_non_daemon__positive_plain__do_match(dummy_context):
    from behave_cmdline.steps import _steps as s

    dummy_context.text = "echo 'SOME OUTPUT'"
    s.i_run_this_command(dummy_context)

    dummy_context.table = Table(headings=["mode", "shows", "value"],
                                rows=[["plain", "Y", "SOME OUTPUT"]])

    # MUST NOT RAISE
    s.i_see_in_the_output_of(dummy_context, stream="stdout")


def test_non_daemon__positive_plain__dont_match(dummy_context):
    from behave_cmdline.steps import _steps as s

    dummy_context.text = "echo 'SOME OUTPUT'"
    s.i_run_this_command(dummy_context)

    dummy_context.table = Table(headings=["mode", "shows", "value"],
                                rows=[["plain", "Y", "**OTHER** OUTPUT"]])

    with pytest.raises(AssertionError):
        s.i_see_in_the_output_of(dummy_context, stream="stdout")


def test_non_daemon__negative_plain__do_match(dummy_context):
    from behave_cmdline.steps import _steps as s

    dummy_context.text = "echo 'SOME OUTPUT'"
    s.i_run_this_command(dummy_context)

    dummy_context.table = Table(headings=["mode", "shows", "value"],
                                rows=[["plain", "N", "SOME OUTPUT"]])

    with pytest.raises(AssertionError):
        s.i_see_in_the_output_of(dummy_context, stream="stdout")


def test_non_daemon__negative_plain__dont_match(dummy_context):
    from behave_cmdline.steps import _steps as s

    dummy_context.text = "echo 'SOME OUTPUT'"
    s.i_run_this_command(dummy_context)

    dummy_context.table = Table(headings=["mode", "shows", "value"],
                                rows=[["plain", "N", "**OTHER** OUTPUT"]])

    # MUST NOT RAISE
    s.i_see_in_the_output_of(dummy_context, stream="stdout")


#
# REGEX MODE
#
def test_non_daemon__positive_regex__do_match(dummy_context):
    from behave_cmdline.steps import _steps as s

    dummy_context.text = "echo 'SOME OUTPUT'"
    s.i_run_this_command(dummy_context)

    dummy_context.table = Table(headings=["mode", "shows", "value"],
                                rows=[["regex", "Y", "SOME ...PUT"]])

    # MUST NOT RAISE
    s.i_see_in_the_output_of(dummy_context, stream="stdout")


def test_non_daemon__positive_regex__dont_match(dummy_context):
    from behave_cmdline.steps import _steps as s

    dummy_context.text = "echo 'SOME OUTPUT'"
    s.i_run_this_command(dummy_context)

    dummy_context.table = Table(headings=["mode", "shows", "value"],
                                rows=[["regex", "Y", "\*\*OTHER\*\* ...PUT"]])

    with pytest.raises(AssertionError):
        s.i_see_in_the_output_of(dummy_context, stream="stdout")


def test_non_daemon__negative_regex__do_match(dummy_context):
    from behave_cmdline.steps import _steps as s

    dummy_context.text = "echo 'SOME OUTPUT'"
    s.i_run_this_command(dummy_context)

    dummy_context.table = Table(headings=["mode", "shows", "value"],
                                rows=[["regex", "N", "SOME ...PUT"]])

    with pytest.raises(AssertionError):
        s.i_see_in_the_output_of(dummy_context, stream="stdout")


def test_non_daemon__negative_regex__dont_match(dummy_context):
    from behave_cmdline.steps import _steps as s

    dummy_context.text = "echo 'SOME OUTPUT'"
    s.i_run_this_command(dummy_context)

    dummy_context.table = Table(headings=["mode", "shows", "value"],
                                rows=[["regex", "N", "\*\*OTHER\*\* ...PUT"]])

    # MUST NOT RAISE
    s.i_see_in_the_output_of(dummy_context, stream="stdout")

#
# PASS BY TIMEOUT
#
def test_daemon__timeout__positive_plain__do_match(dummy_context):
    from behave_cmdline.steps import _steps as s

    dummy_context.text = "sleep 10 && echo 'SOME OUTPUT'"
    s.i_launch_this_daemon(dummy_context)

    dummy_context.table = Table(headings=["mode", "shows", "value"],
                                rows=[["plain", "Y", "SOME OUTPUT"]])

    with pytest.raises(AssertionError):
        s.i_see_in_the_output_of(dummy_context, stream="stdout", timeout=1)


def test_daemon__timeout__negative_plain__do_match(dummy_context):
    from behave_cmdline.steps import _steps as s

    dummy_context.text = "sleep 10 && echo 'SOME OUTPUT'"
    s.i_launch_this_daemon(dummy_context)

    dummy_context.table = Table(headings=["mode", "shows", "value"],
                                rows=[["plain", "N", "SOME OUTPUT"]])

    # MUST NOT RAISE
    s.i_see_in_the_output_of(dummy_context, stream="stdout", timeout=1)


def test_daemon__timeout__positive_regex__do_match(dummy_context):
    from behave_cmdline.steps import _steps as s

    dummy_context.text = "sleep 10 && echo 'SOME OUTPUT'"
    s.i_launch_this_daemon(dummy_context)

    dummy_context.table = Table(headings=["mode", "shows", "value"],
                                rows=[["regex", "Y", "SOME ...PUT"]])

    with pytest.raises(AssertionError):
        s.i_see_in_the_output_of(dummy_context, stream="stdout", timeout=1)


def test_daemon__timeout__negative_regex__do_match(dummy_context):
    from behave_cmdline.steps import _steps as s

    dummy_context.text = "sleep 10 && echo 'SOME OUTPUT'"
    s.i_launch_this_daemon(dummy_context)

    dummy_context.table = Table(headings=["mode", "shows", "value"],
                                rows=[["regex", "N", "SOME ...PUT"]])

    # MUST NOT RAISE
    s.i_see_in_the_output_of(dummy_context, stream="stdout", timeout=1)


#
# DAEMON EARLY EXIT
#
def test_infinite_daemon__positive_plain__do_match(dummy_context):
    from behave_cmdline.steps import _steps as s

    dummy_context.text = "echo 'SOME OUTPUT' && while true; do sleep 1; done"
    s.i_launch_this_daemon(dummy_context)

    dummy_context.table = Table(headings=["mode", "shows", "value"],
                                rows=[["plain", "Y", "SOME OUTPUT"]])

    # MUST NOT RAISE
    s.i_see_in_the_output_of(dummy_context, stream="stdout")


def test_infinite_daemon__positive_regex__do_match(dummy_context):
    from behave_cmdline.steps import _steps as s

    dummy_context.text = "echo 'SOME OUTPUT' && while true; do sleep 1; done"
    s.i_launch_this_daemon(dummy_context)

    dummy_context.table = Table(headings=["mode", "shows", "value"],
                                rows=[["regex", "Y", "SOME ...PUT"]])

    # MUST NOT RAISE
    s.i_see_in_the_output_of(dummy_context, stream="stdout")
