import os
from pathlib import Path

from dlpfs import Loopback


def test_initialization(tmp_path):
    root = os.path.join(Path(__file__).parent, "test-data")
    fs = Loopback(root=root)

    assert fs.root == root


def test_file_write(tmp_path):
    root = Path(os.path.join(Path(tmp_path), "test-data"))

    os.mkdir(root)

    fs = Loopback(root=str(root))

    data = "THIS IS SOME DATA".encode("utf-8")

    fh = fs.__call__("create", "/foo", os.O_CREAT | os.O_WRONLY)

    written_bytes = fs.__call__("write", "/foo", data, 0, fh)

    fs.__call__("release", "/foo", fh)

    assert written_bytes
    assert len(data) == written_bytes
    assert Path(root, "foo").exists


def test_read_file():
    root = Path(Path(__file__).parent, "test-data")

    fs = Loopback(root=str(root))

    fh = fs.__call__("open", "/plain-text.txt", os.O_RDONLY)

    content = fs.__call__("read", "/plain-text.txt", 8 * 1024, 0, fh)

    fs.__call__("release", "/plain-text.txt", fh)

    assert len(content)
