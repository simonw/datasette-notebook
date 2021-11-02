import bleach
from bleach.sanitizer import Cleaner
from bleach.html5lib_shim import Filter
import markdown
from markdown.extensions.wikilinks import WikiLinkExtension, WikiLinksInlineProcessor
from markupsafe import Markup


def render_markdown(value, datasette):
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
            markdown.markdown(
                value,
                output_format="html5",
                extensions=[
                    "fenced_code",
                    CustomWikiLinkExtension(
                        base_url=datasette.urls.path("/n/"),
                        end_url="",
                        build_url=build_url,
                    ),
                ],
            )
        )
    )
    return Markup(html)


class CustomWikiLinkExtension(WikiLinkExtension):
    # Subclassed to support [[foo/bar]] with / in it

    def extendMarkdown(self, md):
        self.md = md

        WIKILINK_RE = r"\[\[([\w0-9_ -\\]+)\]\]"
        wikilinkPattern = WikiLinksInlineProcessor(WIKILINK_RE, self.getConfigs())
        wikilinkPattern.md = md
        md.inlinePatterns.register(wikilinkPattern, "wikilink", 75)


def build_url(label, base, end):
    """ Build a url from the label, a base, and an end. """
    clean_label = label.replace(" ", "_")
    return "{}{}{}".format(base, clean_label, end)


class ImageMaxWidthFilter(Filter):
    """Adds style="max-width: 100%" to any image tags"""

    def __iter__(self):
        for token in Filter.__iter__(self):
            if token["type"] == "EmptyTag" and token["name"] == "img":
                token["data"][(None, "style")] = "max-width: 100%"
            yield token
