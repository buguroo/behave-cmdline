from functools import partial


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


def in_the_output_of(context, stream, alias="default", timeout=float('inf')):
    """
    Busca en la salida `stream` del comando ejecutado las valores
    pasados en la tabla línea a línea, respetando el orden.

        - Columna `logic`: Aparece/No Aparece.
        - Columna `text`: Busca con `in`.
        - Columna `regex`: Busca con `re.match`.

    """
    if 'text' in context.table.headings:
        def matcher(fragment, line):
            return fragment in line
    elif 'regex' in context.table.headings:
        def matcher(regex, line):
            return re.match(regex, line)
    else:
        raise ValueError("Either text or regex is mandatory.")

    checks = []
    for row in context.table:
        must_appear = not row["logic"].lower().startswith("no")
        do_match = partial(matcher, row.get("text", row.get("regex")))

        def check_lines():
            try:
                while True:
                    if do_match((yield)):
                        if not must_appear:
                            assert False, row
                        else:
                            return
            except GeneratorExit as exc:
                if must_appear:
                    assert False, row

        check = check_lines()
        check.send(None)
        checks.append(check)

    context.cmdline_processes[alias].check_stream(
        stream, *checks, timeout=timeout)
