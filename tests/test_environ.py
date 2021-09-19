import os
import pytest

from bddcli import Given, stdout, Application, when, given


def foos():  # pragma: no cover
    e = os.environ.copy()
    print(' '.join(
        f'{k}: {v}' for k, v in e.items() if k not in ['LC_CTYPE', 'PWD']
    ))


app = Application('foo', 'tests.test_environ:foos')


@pytest.mark.skipif(os.name == "nt", reason="On Windows, environment isn't"
                    "emptied")
def test_environ():
    with Given(app, environ={'bar': 'baz'}):
        assert stdout == 'bar: baz\n'

        when(environ=given - 'bar')
        assert stdout == '\n'

        when(environ=given + {'qux': 'quux'})
        assert stdout == 'bar: baz qux: quux\n'

        when(environ=given | {'bar': 'quux'})
        assert stdout == 'bar: quux\n'
