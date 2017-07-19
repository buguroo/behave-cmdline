from datetime import datetime
from datetime import timedelta
import io
import os
import queue
import signal
import subprocess
import threading


class Process:
    def __init__(self, args, env, daemon=False):
        self.args = args
        self.env = env
        self.daemon = daemon

        self.readers = []
        self.stdout = queue.Queue()
        self.stdout_file = io.BytesIO()
        self.stderr = queue.Queue()
        self.stderr_file = io.BytesIO()

        self.start_time = None

    def terminate(self):
        if self.daemon:
            os.killpg(os.getpgid(self.process.pid),
                                 signal.SIGTERM)
            self.process.wait()

    def __enter__(self):
        self.process = subprocess.Popen(
            self.args,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=self.env,
            preexec_fn=os.setpgrp)

        self.readers.append(
            threading.Thread(target=self.read_stream,
                             args=['stdout'],
                             daemon=True))
        self.readers.append(
            threading.Thread(target=self.read_stream,
                             args=['stderr'],
                             daemon=True))

        for reader in self.readers:
            reader.start()

        if not self.daemon:
            self.process.wait()
            assert self.process.returncode == 0, self.process.returncode

        return self

    def __exit__(self, *_):
        self.terminate()

        for reader in self.readers:
            reader.join()

    def read_stream(self, name):
        input_stream = getattr(self.process, name)
        output_queue = getattr(self, name)
        output_file = getattr(self, name + '_file')
        for lineno, line in enumerate(iter(input_stream.readline, b'')):
            if lineno > 0:
                output_file.write(b'\n')
            output_queue.put(line)
            output_file.write(line)

    def check_stream(self, stream, *checks, timeout=None, encoding='utf-8'):
        self.start_time = datetime.today()

        checks = list(checks)

        # Initialize generators
        for check in checks:
            check.send(None)

        input_stream = getattr(self, stream)

        if timeout is None:
            def timedout():
                return False
        else:
            exceeded = self.start_time + timedelta(seconds=timeout)
            def timedout():
                return datetime.today() > exceeded

        while checks and not timedout():
            try:
                line = input_stream.get(block=True, timeout=0.1)
            except queue.Empty:
                if self.process.returncode is not None:
                    # The process exited
                    if any(r.is_alive() for r in self.readers):
                        # Some reader is still running, we wait
                        continue
                    else:
                        # All readers finished, we exit
                        break
            else:
                # If encoding is specified (default), line is decoded;
                # otherwise is bytes.
                if encoding is not None:
                    line = line.decode(encoding)

                for check in checks.copy():
                    try:
                        check.send(line)
                    except StopIteration as exc:
                        # Check success
                        checks.remove(check)

        for check in checks:
            check.close()
