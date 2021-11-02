from datasette.app import Datasette
from datasette_notebook.utils import render_markdown
import pytest
import sqlite3


@pytest.mark.parametrize(
    "input,expected",
    (
        ("# Hello", "<h1>Hello</h1>"),
        ("[[foo]]", '<p><a href="/n/foo" rel="nofollow">foo</a></p>'),
        ("[[foo/bar]]", '<p><a href="/n/foo/bar" rel="nofollow">foo/bar</a></p>'),
    ),
)
def test_render_markdown(input, expected):
    datasette = Datasette([], memory=True)
    output = render_markdown(input, datasette)
    assert output == expected
