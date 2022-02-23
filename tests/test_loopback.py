import os
from pathlib import Path
import pytest

from dlpfs import Loopback


def test_initialization(tmp_path):
    root = os.path.join(Path(__file__).parent, 'test-data')
    fs = Loopback(root=root)

    assert fs.root == root


def test_file_write(tmp_path):
    root = Path(os.path.join(Path(tmp_path), 'test-data'))

    os.mkdir(root)

    fs = Loopback(root=str(root.absolute))

    data = "THIS IS SOME DATA".encode('utf-8')

    fh = fs.open("foo", os.O_CREAT | os.O_WRONLY)

    written_bytes = fs.write("foo", data, 0, fh)

    fs.release("foo", fh)

    assert written_bytes
    assert len(data) == written_bytes
    assert Path(root, "foo").exists


@pytest.mark.skip("To be fixed")
def test_read_file():
    root = Path(Path(__file__).parent, "test-data")

    fs = Loopback(root=str(root.absolute))

    fh = fs.open("plain-text.txt", os.O_RDONLY)

    content = fs.read("plain-text.txt", 8 ** 1024, 0, fh)

    fs.release("plain-text.txt", fh)

    assert len(content)
