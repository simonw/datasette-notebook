from datasette.utils.asgi import Response
from datasette import hookimpl
import sqlite_utils
from .utils import render_markdown


@hookimpl
def startup(datasette):
    # Create tables for notebook DB if needed
    db_name = config_notebook(datasette)
    assert (
        db_name in datasette.databases
    ), "datasette-notebook needs a '{}' database to start".format(db_name)

    def create_tables(conn):
        db = sqlite_utils.Database(conn)
        if not db["pages"].exists():
            db["pages"].create(
                {
                    "slug": str,
                    "content": str,
                },
                pk="slug",
            )

    async def inner():
        await datasette.get_database(db_name).execute_write_fn(
            create_tables, block=True
        )

    return inner


async def notebook(request, datasette):
    slug = request.url_vars.get("slug") or ""
    db_name = config_notebook(datasette)
    db = datasette.get_database(db_name)

    if request.method == "POST":
        vars = await request.post_vars()
        content = vars.get("content")
        if content:
            await db.execute_write(
                "INSERT OR REPLACE INTO pages (slug, content) VALUES(?, ?)",
                [slug, content],
                block=True,
            )
            return Response.redirect(request.path)
        else:
            return Response.html("content= is required", status=400)

    row = (await db.execute("select * from pages where slug = ?", [slug])).first()
    if row is None:
        # Form to create a page
        return Response.html(
            await datasette.render_template(
                "datasette_notebook/edit.html",
                {
                    "slug": slug,
                },
                request=request,
            )
        )

    if slug == "":
        children = await db.execute("select * from pages where slug != ''")
    else:
        children = await db.execute(
            "select * from pages where slug like ?", ["{}/%".format(slug)]
        )

    return Response.html(
        await datasette.render_template(
            "datasette_notebook/view.html",
            {
                "slug": slug,
                "content": row["content"],
                "rendered": render_markdown(row["content"]),
                "children": children.rows,
            },
            request=request,
        )
    )


@hookimpl
def register_routes():
    return [(r"^/n$", notebook), (r"^/n/(?P<slug>.*)$", notebook)]


def config_notebook(datasette):
    config = datasette.plugin_config("datasette-notebook") or {}
    return config.get("database") or "notebook"
