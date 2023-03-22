from abc import ABC, abstractmethod
from os.path import realpath
import os
import re
try:
    import re2
except ImportError:
    import re as re2
from typing import Optional, Tuple

import logging


class FormatProcessor(ABC):
    def __init__(self, path, flags):
        logging.debug(f"Creating debug for {path} and {flags}")
        self.path = realpath(path)
        self.fd = os.open(self.path, flags)

    @abstractmethod
    def readrecord(self) -> Tuple[bytes, int]:
        raise Exception("To be implemented")


class CSVFormatProcessor(FormatProcessor):
    def __init__(self, path, flags, use_google_re2: bool = True):
        super().__init__(path, flags)
        self.buffer = bytes
        self.offset = 0
        self.use_google_re2 = use_google_re2
        if use_google_re2:
            logging.debug("Using google-re2 in CSVFormatProcessor")
            self.ptrn = re2.compile(r"\n")
        else:
            logging.debug("Using standard re in CSVFormatProcessor")
            self.ptrn = re.compile(r"\n")

    def readrecord(self, required_offset=0) -> Tuple[bytes, int]:
        record = bytes()
        offset = self.offset
        BUFFER_SIZE = 4 * 1024
        while True:
            buff = os.pread(self.fd, BUFFER_SIZE, self.offset + len(record))

            if not buff:
                break
            else:
                idx = self.__find_record_split(buff)

                if -1 != idx:
                    record += buff[:(idx + len("\n"))]
                    break
                else:
                    record += buff

        self.offset += len(record)
        return (record, offset)

    def __find_record_split(self, buffer):
        m = self.ptrn.search(buffer.decode())
        if m:
            return m.start()
        return -1


def format_detector(path, flags, use_google_re2) -> Optional[FormatProcessor]:
    extension = path.split(".")[-1].lower()

    if extension == "csv" or False:
        return CSVFormatProcessor(path, flags, use_google_re2)

    logging.info("Unsupported format, proceeding as if it was pure text")

    return None
