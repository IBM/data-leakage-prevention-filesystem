import os
from dlpfs.formats import CSVFormatProcessor
from pathlib import Path


def test_record_extraction():
    test_file = (Path(Path(__file__).parent, 'test.csv').absolute())

    processor = CSVFormatProcessor(test_file, os.O_RDONLY)

    while True:
        (record, _) = processor.readrecord()

        if not record:
            break
