#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# (c) 2016 Björn Ricks <bjoern.ricks@gmail.com>
#
# See LICENSE comming with the source of 'phell' for details.
#

from __future__ import print_function

import uuid
import sys

from phell.utils import to_hex
from phell.mbr import Mbr
from phell.gpt import Gpt


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

        if mbr.is_gpt():
            gpt_data = b.read(Gpt.SIZE)
            gpt = Gpt(gpt_data)

            print("GPT Signature {}".format(to_hex(gpt.signature)))
            print("GPT Revision {}".format(to_hex(gpt.revision)))
            print("GPT Header Size {}".format(to_hex(gpt.header_size)))
            print("GPT Disk UUID {}".format(uuid.UUID(to_hex(gpt.guid))))
            print("GPT Partition Entries {}".format(to_hex(gpt.nr_entries)))
            print("GPT Entry Size {}".format(to_hex(gpt.entry_size)))


if __name__ == "__main__":
    main()

# vim: set ts=4 sw=4 tw=80:
