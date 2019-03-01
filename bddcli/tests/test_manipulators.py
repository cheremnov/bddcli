import os
import sys

import pytest

from bddcli import Command, when, stdout, Application, given, stderr


def baz():  # pragma: no cover
    e = os.environ.copy()
    del e['PWD']
    print(' '.join(f'{k}: {v}' for k, v in e.items()))
    print(' '.join(sys.argv), file=sys.stderr)


app = Application('foo', 'bddcli.tests.test_manipulators:baz')


def test_dict_manipulators():
    with Command(app, environ={'bar': 'baz'}):
        assert stdout == 'bar: baz\n'

        with pytest.raises(ValueError):
            when(environ=given + {'bar': 'qux'})


def test_list_manipulators():
    with Command(app, arguments=['bar']):
        assert stderr == 'foo bar\n'

        with pytest.raises(ValueError):
            when(arguments=given + {'invalid': 'qux'})

        with pytest.raises(ValueError):
            when(arguments=given | {'bar': 'qux'})

        when(arguments=given - 'bar')
        assert stderr == 'foo\n'

        with pytest.raises(ValueError):
            when(arguments=given - 'missing')

        when(arguments=given + ['baz', 'qux', 'quux'])
        assert stderr == 'foo bar baz qux quux\n'

        when(arguments=given - ['bar'])
        assert stderr == 'foo\n'

        class InvalidType:
            pass

        with pytest.raises(TypeError):
            when(arguments=given - InvalidType())

        with pytest.raises(TypeError):
            when(arguments=given | InvalidType())

