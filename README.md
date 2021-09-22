# datasette-notebook

[![PyPI](https://img.shields.io/pypi/v/datasette-notebook.svg)](https://pypi.org/project/datasette-notebook/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-notebook?include_prereleases&label=changelog)](https://github.com/simonw/datasette-notebook/releases)
[![Tests](https://github.com/simonw/datasette-notebook/workflows/Test/badge.svg)](https://github.com/simonw/datasette-notebook/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-notebook/blob/main/LICENSE)

A markdown wiki and dashboarding system for Datasette

This is an **experimental alpha** and everything about it is likely to change.

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-notebook

## Usage

With this plugin you must either run Datasette with a file called `notebook.db`:

    datasette notebook.db --create

Here the `--create` option will create that file if it does not yet exist.

Or you can use some other file name and configure that using `metadata.yml`:

```yaml
plugins:
  datasette-notebook:
    database: otherfile
```
Then run Datasette with `otherfile.db`.

Visit `/n` to create an index page. Visit `/n/name` to create a page with that name.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-notebook
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
