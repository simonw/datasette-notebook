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
