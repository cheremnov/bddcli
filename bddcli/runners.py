import os
import abc
import sys
import subprocess as sp
from os import path


class Runner(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def run(self, arguments=None, environ=None, **kw):  # pragma: no cover
        pass


class SubprocessRunner(Runner):

    def _findbindir(self):
        if os.name == "nt":
            bootstrapper = 'bddcli_bootstrapper'
        else:
            bootstrapper = 'bddcli-bootstrapper'
        for d in sys.path:
            try:
                if bootstrapper in os.listdir(d):
                    return d
            except FileNotFoundError or NotADirectoryError:
                # Nothing guarantees a PATH entry is valid
                pass

    @property
    def bootstrapper(self):
        if os.name == "nt":
            bootstrapper = 'bddcli_bootstrapper'
        else:
            bootstrapper = 'bddcli-bootstrapper'
        if 'VIRTUAL_ENV' in os.environ:
            bindir = path.join(os.environ['VIRTUAL_ENV'], 'bin')
        else:  # pragma: no cover
            bindir = self._findbindir()

        if os.name == "nt":
            return path.join(bindir, bootstrapper, "__init__.py")
        else:
            return path.join(bindir, bootstrapper)

    def __init__(self, application, environ=None):
        self.application = application
        self.environ = environ

    def run(self, arguments=None, working_directory=None, environ=None, **kw):
        command = [
            self.bootstrapper,
            self.application.name,
            self.application.address,
            working_directory or '.',
        ]

        if arguments:
            command += arguments

        if os.name == "nt":
            # On Windows, the specified env must include a valid SystemRoot
            # Use a current value
            if environ is not None:
                environ["SystemRoot"] = os.environ["SystemRoot"]
            process = sp.Popen(
                ' '.join(command),
                stdout=sp.PIPE,
                stderr=sp.PIPE,
                shell=True,
                env=environ,
                **kw,
            )
        else:
            process = sp.Popen(
                ' '.join(command),
                stdout=sp.PIPE,
                stderr=sp.PIPE,
                shell=True,
                env=environ,
                preexec_fn=os.setpgrp,
                **kw,
            )
        return process
