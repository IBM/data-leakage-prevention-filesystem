import argparse
import logging
from dlpfs import DataLeakagePreventionFileSystem
from dlpfs.loopback import Loopback
from os.path import realpath

from fuse import FUSE


def create_fs(args):
    t: str = str(args.t).lower()
    if t == 'loopback':
        print("Creating loopback FS")
        return Loopback(args.r)
    if t == 'ppfs':
        print("Creating ppfs FS")
        logging.info(f'Protecting {realpath(args.r)} with DataLeakagePreventionFileSystem')
        return DataLeakagePreventionFileSystem(args.r, args.s, use_google_re2=args.re2, guard_size=args.g, use_sub=args.sub)

    raise Exception()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', type=str, help='accepted values: loopback, dlpfs', required=True)
    parser.add_argument('-r', type=str, help='root', required=True)
    parser.add_argument('-m', type=str, help='mountpoint', required=True)
    parser.add_argument('-s', type=str, help='protection specs (required for ppfs only)')
    parser.add_argument('-re2', action='store_true', help='use google-re2 instead of re')
    parser.add_argument('-sub', action='store_true', help='use sub instead of finditer for regular expression validation')
    parser.add_argument('-g', type=int, help='guard size in bytes (required for ppfs only)', default=256)
    parser.add_argument('-l', type=str, help='accepted values: CRITICAL,ERROR,WARNING,INFO,DEBUG', default='ERROR')

    args = parser.parse_args()

    logging.basicConfig(level=logging.getLevelName(args.l))

    fs = create_fs(args)

    fuse = FUSE(fs, args.m, foreground=True)
