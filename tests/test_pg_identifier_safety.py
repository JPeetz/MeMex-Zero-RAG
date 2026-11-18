"""SQL identifier validation.

Table names cannot be bound as query parameters, so they must be interpolated — which makes
validation the only defence against an identifier being used to break out of the statement.
"""

import pytest


def test_valid_identifiers_accepted(memex_pg_backend_module):
    for name in ("npi_pages", "pages", "_private", "a1", "A" * 63):
        assert memex_pg_backend_module._safe_ident(name) == name


def test_injection_shaped_identifiers_rejected(memex_pg_backend_module):
    bad = [
        "pages; DROP TABLE users",
        "pages--",
        "pages/*x*/",
        "pages) UNION SELECT 1",
        '"pages"',
        "pages\n",
        "",
        "1pages",
        "a" * 64,
        "pages schema",
    ]
    for name in bad:
        with pytest.raises(ValueError):
            memex_pg_backend_module._safe_ident(name)


def test_constructor_validates_table(memex_pg_backend_module):
    """The choke point is __init__: an unsafe table name must never reach a query."""
    with pytest.raises(ValueError):
        memex_pg_backend_module.PostgresSearchEngine(wiki_path=".", dsn="", table="x; DROP TABLE y")
