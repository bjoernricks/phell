#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# (c) 2016 Björn Ricks <bjoern.ricks@gmail.com>
#
# See LICENSE comming with the source of 'phell' for details.
#

from __future__ import print_function

import sys

from phell.utils import to_hex
from phell.mbr import Mbr


def main():
    if len(sys.argv) < 2:
        sys.exit(1)

    disk = sys.argv[1]

    with open(disk, "rb") as b:
        data = b.read(Mbr.SIZE)

    mbr = Mbr(data)

    print("Disk Signature {}".format(to_hex(mbr.disk_signature)))

    if mbr.is_protected():
        print("MBR is protected")

    if mbr.is_gpt():
        print("GUID Partition Table is used")

    print("Null {}".format(to_hex(mbr.null)))
    print("Boot Signature {}".format(to_hex(mbr.boot_signature)))
    print()

    for i, partition in enumerate(mbr.partitions):
        print("Partition {}\n{}\n".format(i, partition))


if __name__ == "__main__":
    main()

# vim: set ts=4 sw=4 tw=80:
