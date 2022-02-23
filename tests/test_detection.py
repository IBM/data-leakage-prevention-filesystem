import pytest
from dlpfs.detection import build_rule


def test_regex_python():
    matcher = build_rule({"type": "re", "spec": "FOO"}, use_google_re2=False)

    match = [m.group() for m in matcher.finditer("THIS IS SOMETHING IN WHICH FOO IS CONTAINED")]

    assert match
    assert len(match)
    assert match[0] == "FOO"


def test_regex_re2():
    matcher = build_rule({"type": "re", "spec": "FOO"}, use_google_re2=True)

    match = [m.group() for m in matcher.finditer("THIS IS SOMETHING IN WHICH FOO IS CONTAINED")]

    assert match
    assert len(match)
    assert match[0] == "FOO"


def test_lookup():
    matcher = build_rule({"type": "lookup", "spec": ["FOO", "BAR"]})

    match = [m.group() for m in matcher.finditer("THIS IS SOMETHING IN WHICH FOO IS CONTAINED")]

    assert match
    assert len(match)
    assert match[0] == "FOO"

    match = [m.group() for m in matcher.finditer("THIS IS SOMETHING IN WHICH BAR IS CONTAINED")]

    assert match
    assert len(match)
    assert match[0] == "BAR"


def test_lookup_converted_python():
    matcher = build_rule({"type": "lookup", "spec": ["FOO", "BAR"]})

    match = [m.group() for m in matcher.finditer("THIS IS SOMETHING IN WHICH FOO IS CONTAINED")]

    assert match
    assert len(match)
    assert match[0] == "FOO"

    match = [m.group() for m in matcher.finditer("THIS IS SOMETHING IN WHICH FOO IS CONTAINED")]

    assert match
    assert len(match)
    assert match[0] == "FOO"


def test_lookup_converted_re2():
    matcher = build_rule({"type": "lookup", "spec": ["FOO", "BAR"]}, use_google_re2=True)

    match = [m.group() for m in matcher.finditer("THIS IS SOMETHING IN WHICH FOO IS CONTAINED")]

    assert match
    assert len(match)
    assert match[0] == "FOO"

    match = [m.group() for m in matcher.finditer("THIS IS SOMETHING IN WHICH FOO IS CONTAINED")]

    assert match
    assert len(match)
    assert match[0] == "FOO"


def test_not_supported():
    with pytest.raises(ValueError) as excinfo:
        _ = build_rule({"type": "FOO", "spec": "BAR"})

    assert "FOO" in str(excinfo)
