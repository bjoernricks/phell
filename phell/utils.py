# -*- coding: utf-8 -*-
#
# (c) 2016 Björn Ricks <bjoern.ricks@gmail.com>
#
# See LICENSE comming with the source of 'phell' for details.
#
import sys


def to_hex(value):
    if sys.version_info.major < 3:
        return value.encode('hex')
    return "".join("%02x" % b for b in value)


def from_hex(value):
    if sys.version_info.major < 3:
        return value.decode('hex')
    return bytes.fromhex(value)


def swap_bytes(value):
    if sys.version_info.major < 3:
        return "".join([bytes(b) for b in reversed(value)])
    return bytes(reversed(value))

# vim: set ts=4 sw=4 tw=80:
