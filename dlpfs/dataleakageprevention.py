from errno import EBADF

from fuse import FuseOSError

import json
import os

import logging

from .loopback import Loopback
from .detection import compile_transformation
from .formats import FormatProcessor, format_detector


class FD:
    def __init__(self, fd: int, processor: FormatProcessor):
        self.buffer = bytes()
        self.fd = fd
        self.read_pointer = 0
        self.write_pointer = 0
        self.need_write = False
        self.processor = processor
        self.offset = 0


class DataLeakagePreventionFileSystem(Loopback):
    def __init__(self, root, ruleSpecs, use_google_re2=False, guard_size=0, use_sub=False):
        super().__init__(root)
        with open(ruleSpecs) as infile:
            config = json.load(infile)
        self.rules = compile_transformation(config, use_google_re2)
        self.protect_read = config.get('do_read', True)
        self.protect_write = config.get('do_write', True)
        self.open_files = {}
        self.use_google_re2 = use_google_re2
        self.guard_size = guard_size
        self.use_sub = use_sub

    def open(self, path, flags):
        logging.info('Opening file {} as {}'.format(path, flags))
        fd = os.open(path, flags)
        self.open_files[fd] = FD(fd, format_detector(path, flags, self.use_google_re2))
        return fd

    def flush(self, path, fh):
        pass

    def create(self, path, mode=511):
        logging.info('Creating file {}'.format(path))
        ref = self.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
        return ref

    def read(self, path, size, offset, fh):
        logging.info(f'Reading from {fh} with parmas: {path} {size} {offset}')

        if fh not in self.open_files:
            raise FuseOSError(EBADF)
        if self.protect_read:
            logging.info('Read for this file is protected')

            return self.__protect_with_guard(fh, offset, size)
        else:
            return os.read(fh, size)

    def __protect_with_guard(self, fd, offset, size):
        fake_offset = max(0, offset - self.guard_size)
        offset_diff = offset - fake_offset
        fake_size = offset_diff + size + self.guard_size

        buff = os.pread(fd, fake_size, fake_offset)

        if len(buff):
            return self.__sanitize(buff)[offset_diff:offset_diff + size]
        return buff

    def write(self, path, data: bytes, offset, fh):
        logging.info(f'Writing to {fh}')

        if fh not in self.open_files:
            raise FuseOSError(EBADF)

        _fd = self.open_files[fh]

        if self.protect_write:
            _fd.buffer = _fd.buffer[:offset].ljust(offset, '\x00'.encode('ascii')) + data + _fd.buffer[offset + len(data):]
            data = self.__sanitize(data)

        os.lseek(fh, offset, 0)
        return os.write(fh, data)

    def release(self, path, fh):
        logging.info('Releasing {}'.format(fh))

        _fd = self.open_files[fh]

        if _fd.need_write:
            logging.debug('Write protected')
            _fd.buffer = self.__sanitize(_fd.buffer)
            logging.debug('Flushing buffer')
            os.write(fh, _fd.buffer)
            logging.debug('Written')

        del self.open_files[fh]
        return os.close(fh)

    def __sanitize(self, buffer: bytes) -> bytes:
        logging.info('Removing required patterns')
        text = buffer.decode()

        for spec in self.rules:
            logging.info(f'Applying {spec}')
            transformation = spec['transformation']
            for rule in spec['rules']:
                matched = False
                if self.use_sub:
                    text2 = rule.sub(lambda m: transformation(m.group(0)), text)
                    matched = text == text2
                    text = text2
                else:
                    for m in rule.finditer(text):
                        text = text[0:m.start()] + transformation(m.group(0)) + text[m.end():]
                if matched:
                    break
        return text.encode()

    @staticmethod
    def __read_all(fd: int) -> bytes:
        logging.info('Reading all content')
        buffer = bytes()
        BUFFER_SIZE = 16 * 1024 * 1024

        while True:
            buff = os.read(fd, BUFFER_SIZE)
            if buff:
                buffer += buff
            else:
                break
        logging.info('Returning buffer')
        return buffer
