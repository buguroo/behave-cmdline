def _plain_matcher(fragment, line):
    return fragment in line


def _regex_matcher(regex, line):
    import re
    return re.match(regex, line)


def _check_lines(do_match, shows, row):
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


def i_see_the_string(context, string):
    from functools import partial
    do_match = partial(_plain_matcher, string)
    check = _check_lines(do_match, shows=True, string)
    yield from check


def i_dont_see_the_string(context, string):
    from functools import partial
    do_match = partial(_plain_matcher, string)
    check = _check_lines(do_match, shows=False, string)
    yield from check


def the_regex_matches(context, regex):
    from functools import partial
    do_match = partial(_regex_matcher, regex)
    check = _check_lines(do_match, shows=True, regex)
    yield from check


def the_regex_doesnt_match(context, regex):
    from functools import partial
    do_match = partial(_regex_matcher, regex)
    check = _check_lines(do_match, shows=False, regex)
    yield from check
