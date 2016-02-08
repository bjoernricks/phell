# -*- coding: utf-8 -*-
#
# (c) 2016 Björn Ricks <bjoern.ricks@gmail.com>
#
# See LICENSE comming with the source of 'phell' for details.
#

import uuid

from phell.utils import to_int, from_hex


class Gpt(object):

    SIZE = 512
    EFI_SIGNATURE = from_hex("4546492050415254")
    EFI_REVISION = from_hex("00000100")

    SIGNATURE_START = 0
    SIGNATURE_SIZE = 8
    SIGNATURE_END = SIGNATURE_START + SIGNATURE_SIZE

    REVISION_START = SIGNATURE_END
    REVISION_SIZE = 4
    REVISION_END = REVISION_START + REVISION_SIZE

    HEADER_SIZE_START = REVISION_END
    HEADER_SIZE_SIZE = 4
    HEADER_SIZE_END = HEADER_SIZE_START + HEADER_SIZE_SIZE

    HEADER_CRC_START = HEADER_SIZE_END
    HEADER_CRC_SIZE = 4
    HEADER_CRC_END = HEADER_CRC_START + HEADER_CRC_SIZE

    RESERVED_START = HEADER_CRC_END
    RESERVED_SIZE = 4
    RESERVED_END = RESERVED_START + RESERVED_SIZE

    CURRENT_LBA_START = RESERVED_END
    CURRENT_LBA_SIZE = 8
    CURRENT_LBA_END = CURRENT_LBA_START + CURRENT_LBA_SIZE

    BACKUP_LBA_START = CURRENT_LBA_END
    BACKUP_LBA_SIZE = 8
    BACKUP_LBA_END = BACKUP_LBA_START + BACKUP_LBA_SIZE

    FIRST_LBA_START = BACKUP_LBA_END
    FIRST_LBA_SIZE = 8
    FIRST_LBA_END = FIRST_LBA_START + FIRST_LBA_SIZE

    LAST_LBA_START = FIRST_LBA_END
    LAST_LBA_SIZE = 8
    LAST_LBA_END = LAST_LBA_START + LAST_LBA_SIZE

    GUID_START = LAST_LBA_END
    GUID_SIZE = 16
    GUID_END = GUID_START + GUID_SIZE

    STARTING_LBA_START = GUID_END
    STARTING_LBA_SIZE = 8
    STARTING_LBA_END = STARTING_LBA_START + STARTING_LBA_SIZE

    NUMBER_ENTRIES_START = STARTING_LBA_END
    NUMBER_ENTRIES_SIZE = 4
    NUMBER_ENTRIES_END = NUMBER_ENTRIES_START + NUMBER_ENTRIES_SIZE

    ENTRY_SIZE_START = NUMBER_ENTRIES_END
    ENTRY_SIZE_SIZE = 4
    ENTRY_SIZE_END = ENTRY_SIZE_START + ENTRY_SIZE_SIZE

    PARTITIONS_CRC_START = ENTRY_SIZE_END
    PARTITIONS_CRC_SIZE = 4
    PARTITIONS_CRC_END = PARTITIONS_CRC_START + PARTITIONS_CRC_SIZE

    def __init__(self, data):
        self.data = data
        self.signature = data[Gpt.SIGNATURE_START:Gpt.SIGNATURE_END]
        self.revision = data[Gpt.REVISION_START:Gpt.REVISION_END]
        self.header_size = to_int(data[
            Gpt.HEADER_SIZE_START:Gpt.HEADER_SIZE_END])
        self.header_crc = data[Gpt.HEADER_CRC_START:Gpt.HEADER_CRC_END]
        self.current_lba = to_int(data[
            Gpt.CURRENT_LBA_START:Gpt.CURRENT_LBA_END])
        self.backup_lba = to_int(data[
            Gpt.BACKUP_LBA_START:Gpt.BACKUP_LBA_END])
        self.first_lba = to_int(data[
            Gpt.FIRST_LBA_START:Gpt.FIRST_LBA_END])
        self.last_lba = to_int(data[
            Gpt.LAST_LBA_START:Gpt.LAST_LBA_END])
        self.guid = uuid.UUID(bytes_le=data[Gpt.GUID_START:Gpt.GUID_END])
        self.start_lba = to_int(data[
            Gpt.STARTING_LBA_START:Gpt.STARTING_LBA_END])
        self.nr_entries = to_int(data[
            Gpt.NUMBER_ENTRIES_START:Gpt.NUMBER_ENTRIES_END])
        self.entry_size = to_int(data[
            Gpt.ENTRY_SIZE_START:Gpt.ENTRY_SIZE_END])
        self.partitions_crc = \
            data[Gpt.PARTITIONS_CRC_START:Gpt.PARTITIONS_CRC_END]

    def is_valid(self):
        # todo:
        #  - Check the Signature
        #  - Check the Header CRC
        #  - Check that the current LBA entry points to the LBA that contains
        #    the GUID Partition Table
        #  - Check the CRC of the GUID Partition Entry Array
        # If the GPT is the primary table, stored at LBA 1:
        #  - Check the Backup LBA to see if it is a valid GPT
        return True


class GptPartition(object):

    DEFAULT_SIZE = 128

    def __init__(self, data):
        pass

# vim: set ts=4 sw=4 tw=80:
