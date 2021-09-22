import bleach
from bleach.sanitizer import Cleaner
from bleach.html5lib_shim import Filter
import markdown
from markupsafe import Markup


def render_markdown(value):
    attributes = {"a": ["href"], "img": ["src", "alt"]}
    cleaner = Cleaner(
        tags=[
            "a",
            "abbr",
            "acronym",
            "b",
            "blockquote",
            "code",
            "em",
            "i",
            "li",
            "ol",
            "strong",
            "ul",
            "pre",
            "p",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "img",
        ],
        attributes=attributes,
        filters=[ImageMaxWidthFilter],
    )
    html = bleach.linkify(
        cleaner.clean(
            markdown.markdown(value, output_format="html5", extensions=["fenced_code"])
        )
    )
    return Markup(html)


class ImageMaxWidthFilter(Filter):
    """Adds style="max-width: 100%" to any image tags"""

    def __iter__(self):
        for token in Filter.__iter__(self):
            if token["type"] == "EmptyTag" and token["name"] == "img":
                token["data"][(None, "style")] = "max-width: 100%"
            yield token
