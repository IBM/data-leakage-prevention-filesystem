import os
from pathlib import Path
from pytest import fail

from dlpfs import Loopback


def test_end_to_end():
    fail("Not implemented yet")


def test_initialization(tmp_path):
    root = os.path.join(Path(__file__).parent, 'test-data')
    fs = Loopback(root=root)

    assert fs.root == root


def test_file_write(tmp_path):
    root = root = os.path.join(Path(tmp_path), 'test-data')

    print(root)

    fs = Loopback(root=root)

    fs.write("foo")
