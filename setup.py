from setuptools import setup
import os

VERSION = "0.1a0"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-notebook",
    description="A markdown wiki and dashboarding system for Datasette",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/datasette-notebook",
    project_urls={
        "Issues": "https://github.com/simonw/datasette-notebook/issues",
        "CI": "https://github.com/simonw/datasette-notebook/actions",
        "Changelog": "https://github.com/simonw/datasette-notebook/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["datasette_notebook"],
    entry_points={"datasette": ["notebook = datasette_notebook"]},
    install_requires=["datasette", "sqlite-utils", "markdown", "bleach"],
    extras_require={"test": ["pytest", "pytest-asyncio"]},
    tests_require=["datasette-notebook[test]"],
    package_data={"datasette_notebook": ["static/*", "templates/*"]},
    python_requires=">=3.6",
)
