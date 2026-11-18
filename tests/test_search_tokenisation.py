"""Search must survive punctuation.

`wiki_search("subscriptions/listen")` used to return nothing: FTS5 read the slash as syntax,
raised, and the fallback did a literal phrase match that could never succeed. Slash-bearing
identifiers are normal in MCP (tools/call, resources/read), so this was a silent correctness
bug in the most-used tool in the server.
"""

import pytest

from memex_mcp.search import build_fts_query


@pytest.mark.parametrize("raw,expected", [
    ("subscriptions/listen", '"subscriptions" "listen"'),
    ("tools/call resultType", '"tools" "call" "resultType"'),
    ("input_required", '"input_required"'),
    ("  spaced   out  ", '"spaced" "out"'),
])
def test_punctuation_is_tokenised_not_parsed(raw, expected):
    assert build_fts_query(raw) == expected


def test_operator_injection_is_neutralised():
    """An FTS5 operator typed by a caller must not become syntax."""
    assert build_fts_query("NEAR(a b)") == '"NEAR" "a" "b"'
    assert build_fts_query('x OR y') == '"x" "OR" "y"'
    assert build_fts_query("*") == ""


def test_empty_query_yields_empty_expression():
    assert build_fts_query("") == ""
    assert build_fts_query("/-+*/") == ""
