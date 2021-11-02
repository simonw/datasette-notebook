from datasette.app import Datasette
import pytest
import sqlite3


@pytest.mark.asyncio
async def test_404_if_no_notebook_database():
    datasette = Datasette([], memory=True)
    response = await datasette.client.get("/n")
    assert response.status_code == 404
    assert "Could not find database: notebook" in response.text


@pytest.mark.asyncio
async def test_successful_startup(tmpdir):
    notebook_db = str(tmpdir / "notebook.db")
    sqlite3.connect(notebook_db).execute("vacuum")
    datasette = Datasette([notebook_db])
    await datasette.invoke_startup()
    response = await datasette.client.get("/n")
    assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.parametrize("enabled", (True, False))
async def test_menu_link(tmpdir, enabled):
    files = []
    if enabled:
        notebook_db = str(tmpdir / "notebook.db")
        sqlite3.connect(notebook_db).execute("vacuum")
        files = [notebook_db]
    datasette = Datasette(files)
    response = await datasette.client.get("/")
    assert response.status_code == 200
    fragment = '<li><a href="/n">Notebook</a></li>'
    if enabled:
        assert fragment in response.text
    else:
        assert fragment not in response.text
