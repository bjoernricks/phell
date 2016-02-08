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

    TYPE_GUID_START = 0
    TYPE_GUID_SIZE = 16
    TYPE_GUID_END = TYPE_GUID_START + TYPE_GUID_SIZE

    UNIQUE_GUID_START = TYPE_GUID_END
    UNIQUE_GUID_SIZE = 16
    UNIQUE_GUID_END = UNIQUE_GUID_START + UNIQUE_GUID_SIZE

    FIRST_LBA_START = UNIQUE_GUID_END
    FIRST_LBA_SIZE = 8
    FIRST_LBA_END = FIRST_LBA_START + FIRST_LBA_SIZE

    LAST_LBA_START = FIRST_LBA_END
    LAST_LBA_SIZE = 8
    LAST_LBA_END = LAST_LBA_START + LAST_LBA_SIZE

    ATTRIBUTE_FLAGS_START = LAST_LBA_END
    ATTRIBUTE_FLAGS_SIZE = 8
    ATTRIBUTE_FLAGS_END = ATTRIBUTE_FLAGS_START + ATTRIBUTE_FLAGS_SIZE

    NAME_START = ATTRIBUTE_FLAGS_END
    NAME_SIZE = 72
    NAME_END = NAME_START + NAME_SIZE

    EFI_SYSTEM_TYPE = uuid.UUID("c12a7328-f81f-11d2-ba4b-00a0c93ec93b")
    UNUSED_TYPE = uuid.UUID("00000000-0000-0000-0000-000000000000")
    MBR_TYPE = uuid.UUID("024DEE41-33E7-11D3-9D69-0008C781F39F")
    BIOS_TYPE = uuid.UUID("21686148-6449-6E6F-744E-656564454649")
    MAC_OS_HFS_TYPE = uuid.UUID("48465300-0000-11AA-AA11-00306543ECAC")
    MAC_OS_UFS_TYPE = uuid.UUID("55465300-0000-11AA-AA11-00306543ECAC")
    MAC_OS_BOOT_TYPE = uuid.UUID("426F6F74-0000-11AA-AA11-00306543ECAC")
    LINUX_FILESYSTEM_TYPE = uuid.UUID("0FC63DAF-8483-4772-8E79-3D69D8477DE4")
    LINUX_RAID_TYPE = uuid.UUID("A19D880F-05FC-4D3B-A006-743F0F84911E")
    LINUX_ROOT_X86_TYPE = uuid.UUID("44479540-F297-41B2-9AF7-D131D5F0458A")
    LINUX_ROOT_X86_64_TYPE = uuid.UUID("4F68BCE3-E8CD-4DB1-96E7-FBCAF984B709")
    LINUX_ROOT_ARM_TYPE = uuid.UUID("69DAD710-2CE4-4E3C-B16C-21A1D49ABED3")
    LINUX_ROOT_ARM64_TYPE = uuid.UUID("B921B045-1DF0-41C3-AF44-4C6F280D3FAE")
    LINUX_SWAP_TYPE = uuid.UUID("0657FD6D-A4AB-43C4-84E5-0933C84B4F4F")
    LINUX_LVM_TYPE = uuid.UUID("E6D6D379-F507-44C2-A23C-238F2A3DF928")
    LINUX_HOME_TYPE = uuid.UUID("933AC7E1-2EB4-4F13-B844-0E14E2AEF915")
    LINUX_DMCRYPT_TYPE = uuid.UUID("7FFEC5C9-2D00-49B7-8941-3EA10A5586B7")
    LINUX_LUKS_TYPE = uuid.UUID("CA7D7CCB-63ED-4C53-861C-1742536059CC")

    partition_types = {
        EFI_SYSTEM_TYPE: "EFI System Partition",
        UNUSED_TYPE: "Unused",
        MBR_TYPE: "MBR Partition Scheme",
        BIOS_TYPE: "BIOS Boot Partition",
        MAC_OS_HFS_TYPE: "Mac OS X (HFS/HFS+)",
        MAC_OS_UFS_TYPE: "Mac OS X (UFS)",
        MAC_OS_BOOT_TYPE: "Mac OS X (boot)",
        LINUX_FILESYSTEM_TYPE: "Linux Filesystem",
        LINUX_RAID_TYPE: "Linux RAID",
        LINUX_ROOT_X86_TYPE: "Linux Root (x86)",
        LINUX_ROOT_X86_64_TYPE: "Linux Root (x86-64)",
        LINUX_ROOT_ARM_TYPE: "Linux Root (ARM)",
        LINUX_ROOT_ARM64_TYPE: "Linux Root (ARM64)",
        LINUX_SWAP_TYPE: "Linux Swap",
        LINUX_LVM_TYPE: "Linux LVM",
        LINUX_HOME_TYPE: "Linux /home",
        LINUX_DMCRYPT_TYPE: "Linux dm-crypt",
        LINUX_LUKS_TYPE: "Linux LUKS",
    }

    def __init__(self, data):
        self.data = data
        self.type_guid = uuid.UUID(bytes_le=data[
            self.TYPE_GUID_START:self.TYPE_GUID_END])
        self.unique_guid = uuid.UUID(bytes_le=data[
            self.UNIQUE_GUID_START:self.UNIQUE_GUID_END])
        self.first_lba = to_int(data[
            self.FIRST_LBA_START:self.FIRST_LBA_END])
        self.last_lba = to_int(data[
            self.LAST_LBA_START:self.LAST_LBA_END])
        self.attribute_flags = \
            data[self.ATTRIBUTE_FLAGS_START:self.ATTRIBUTE_FLAGS_END]
        self.name = data[self.NAME_START:self.NAME_END].decode("utf_16_le")

    def is_type(self, ptype_guid):
        return self.type_guid == ptype_guid

    def get_partition_type(self):
        return self.partition_types.get(self.type_guid, "unkown")

# vim: set ts=4 sw=4 tw=80:
