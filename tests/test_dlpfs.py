import os
from pathlib import Path

from dlpfs import DataLeakagePreventionFileSystem


def test_initialization(tmp_path):
    root = os.path.join(Path(__file__).parent, "test-data")
    rule_specs = os.path.join(Path(__file__).parent, "test-rules.json")

    fs = DataLeakagePreventionFileSystem(root=root, rule_specs=rule_specs, use_re2=True, guard_size=1024, use_sub=True)

    assert fs.root == root


def test_file_write(tmp_path):
    root = os.path.join(tmp_path, "test-data")
    rule_specs = os.path.join(Path(__file__).parent, "test-rules.json")

    os.mkdir(root)

    fs = DataLeakagePreventionFileSystem(root=root, rule_specs=rule_specs, use_re2=True, guard_size=1024, use_sub=True)

    data = "THIS IS SOME DATA".encode("utf-8")

    fh = fs.__call__("create", "/foo", os.O_CREAT | os.O_WRONLY)

    written_bytes = fs.__call__("write", "/foo", data, 0, fh)

    fs.__call__("release", "/foo", fh)

    assert written_bytes
    assert len(data) == written_bytes
    assert Path(root, "foo").exists


def test_read_file():
    root = os.path.join(Path(__file__).parent, "test-data")
    rule_specs = os.path.join(Path(__file__).parent, "test-rules.json")

    fs = DataLeakagePreventionFileSystem(root=root, rule_specs=rule_specs, use_re2=True, guard_size=1024, use_sub=True)

    fh = fs.__call__("open", "/plain-text.txt", os.O_RDONLY)

    content = fs.__call__("read", "/plain-text.txt", 8 * 1024, 0, fh)

    fs.__call__("release", "/plain-text.txt", fh)

    assert len(content)
    assert -1 != str(content, encoding="utf-8").find("my_email@foo.bar")


def test_read_with_block():
    root = os.path.join(Path(__file__).parent, "test-data")
    rule_specs = os.path.join(Path(__file__).parent, "test-rules-1.json")

    fs = DataLeakagePreventionFileSystem(root=root, rule_specs=rule_specs, use_re2=True, guard_size=1024, use_sub=True)

    fh = fs.__call__("open", "/plain-text.txt", os.O_RDONLY)

    content: bytes = fs.__call__("read", "/plain-text.txt", 8 * 1024, 0, fh)

    fs.__call__("release", "/plain-text.txt", fh)

    assert len(content)
    assert -1 == str(content, encoding="utf-8").find("my_email@foo.bar")
    assert -1 != str(content, encoding="utf-8").find("".join(["*" for _ in range(len("my_email@foo.bar"))]))
