# -*- coding: utf-8 -*-
#
# (c) 2016 Björn Ricks <bjoern.ricks@gmail.com>
#
# See LICENSE comming with the source of 'phell' for details.
#

from phell.utils import to_hex, from_hex


class MbrPartition(object):

    STATUS_BOOTABLE = from_hex("80")
    LBA_SIZE = 512

    EMPTY_TYPE = from_hex("00")
    FAT12_TYPE = from_hex("01")
    FAT16_TYPE = from_hex("04")
    EXCHS_TYPE = from_hex("05")
    FAT16_32_TYPE = from_hex("06")
    NTFS_TYPE = NTFS_TYPE = HPFS_TYPE = from_hex("07")
    FAT32_CHS_TYPE = from_hex("0b")
    FAT32_LBS_TYPE = from_hex("0c")
    FAT16B_TYPE = from_hex("0e")
    EXT_PART_TYPE = from_hex("0f")
    WIN_RE_TYPE = from_hex("27")
    MINIX_OLD_TYPE = from_hex("80")
    MINIX_TYPE = from_hex("81")
    LINUX_SWAP_TYPE = from_hex("82")
    LINUX_NATIVE_TYPE = from_hex("83")
    LINUX_EXT_TYPE = from_hex("85")
    LINUX_LVM_TYPE = from_hex("8e")
    BSD_TYPE = from_hex("a5")
    OPENBSD_TYPE = from_hex("a6")
    MAC_OS_UFS_TYPE = from_hex("a8")
    NETBSD_TYPE = from_hex("a9")
    MAC_OS_BOOT_TYPE = from_hex("ab")
    MAC_OS_HFS_TYPE = from_hex("af")
    LINUX_LUKS_TYPE = from_hex("e8")
    GPT_TYPE = from_hex("ee")
    EFI_TYPE = from_hex("ef")
    LINUX_LVM_OLD_TYPE = from_hex("fe")

    partition_types = {
        EMPTY_TYPE: "empty",
        FAT12_TYPE: "FAT12",
        FAT16_TYPE: "FAT16 (<=32M)",
        EXCHS_TYPE: "Extended Partition (CHS)",
        FAT16_32_TYPE: "FAT16 (>32M)",
        NTFS_TYPE: "NTFS/exFAT/HPFS",
        FAT32_CHS_TYPE: "FAT32 (CHS)",
        FAT32_LBS_TYPE: "FAT32 (LBA)",
        FAT16B_TYPE: "FAT16B (LBA)",
        EXT_PART_TYPE: "Extended Partition (LBA)",
        WIN_RE_TYPE: "Windows Recovery Environment",
        MINIX_OLD_TYPE: "Minix (old)",
        MINIX_TYPE: "Minix",
        LINUX_SWAP_TYPE: "Linux (swap)",
        LINUX_NATIVE_TYPE: "Linux (native)",
        LINUX_EXT_TYPE: "Linux (extended)",
        LINUX_LVM_TYPE: "Linux (LVM)",
        BSD_TYPE: "BSD",
        OPENBSD_TYPE: "OpenBSD",
        MAC_OS_UFS_TYPE: "Mac OS X (UFS)",
        NETBSD_TYPE: "NetBSD",
        MAC_OS_BOOT_TYPE: "Mac OS X (boot)",
        MAC_OS_HFS_TYPE: "Mac OS X (HFS/HFS+)",
        LINUX_LUKS_TYPE: "Linux (LUKS)",
        GPT_TYPE: "GPT Protected MBR",
        EFI_TYPE: "EFI System Patition",
        LINUX_LVM_OLD_TYPE: "Linux (old LVM)",
    }

    STATUS_START = 0
    STATUS_SIZE = 1
    STATUS_END = STATUS_START + STATUS_SIZE

    CHS_START_START = STATUS_END
    CHS_START_SIZE = 3
    CHS_START_END = CHS_START_START + CHS_START_SIZE

    TYPE_START = CHS_START_END
    TYPE_SIZE = 1
    TYPE_END = TYPE_START + TYPE_SIZE

    CHS_END_START = TYPE_END
    CHS_END_SIZE = 3
    CHS_END_END = CHS_END_START + CHS_END_SIZE

    LBA_START = CHS_END_END
    LBA_SIZE = 4
    LBA_END = LBA_START + LBA_SIZE

    SECTORS_START = LBA_END
    SECTORS_SIZE = 4
    SECTORS_END = SECTORS_START + SECTORS_SIZE

    def __init__(self, data):
        self.data = data
        self.status = data[self.STATUS_START:self.STATUS_END]
        self.chs_start = data[self.CHS_START_START:self.CHS_START_END]
        self.type = data[self.TYPE_START:self.TYPE_END]
        self.chs_end = data[self.CHS_END_START:self.CHS_END_END]
        self.lba = data[self.LBA_START:self.LBA_END]
        self.sectors = data[self.SECTORS_START:self.SECTORS_END]

    def is_bootable(self):
        return self.status == MbrPartition.STATUS_BOOTABLE

    def is_type(self, ptype):
        return self.type == ptype

    def get_partition_type(self):
        return self.partition_types.get(self.type, "unkown")

    def __str__(self):
        return "Data {}\nStatus {} is bootable {}\nType {} " \
            "{}".format(to_hex(self.data), to_hex(self.status),
                        self.is_bootable(), to_hex(self.type),
                        self.get_partition_type())


class Mbr(object):

    SIZE = 512
    PROTECTED = from_hex("5A5A")

    DISK_SIGNATURE_START = 440
    DISK_SIGNATURE_SIZE = 4
    DISK_SIGNATURE_END = DISK_SIGNATURE_START + DISK_SIGNATURE_SIZE

    NULL_START = DISK_SIGNATURE_END  # 444
    NULL_SIZE = 2
    NULL_END = NULL_START + NULL_SIZE

    PARTITION_COUNT = 4
    PARTITION_SIZE = 16
    PARTITION_ENTRIES_START = NULL_END  # 446
    PARTITION_ENTRIES_END = PARTITION_ENTRIES_START + \
        (PARTITION_COUNT * PARTITION_SIZE)

    BOOT_SIGNATURE_START = PARTITION_ENTRIES_END
    BOOT_SIGNATURE_SIZE = 2
    BOOT_SIGNATURE_END = BOOT_SIGNATURE_START + BOOT_SIGNATURE_SIZE
    BOOT_SIGNATURE_MBR = from_hex("55AA")

    def __init__(self, data):
        self.data = data
        self.disk_signature = data[
            Mbr.DISK_SIGNATURE_START:Mbr.DISK_SIGNATURE_END]
        self.null = data[Mbr.NULL_START:Mbr.NULL_END]
        self.boot_signature = data[
            Mbr.BOOT_SIGNATURE_START:Mbr.BOOT_SIGNATURE_END]

        self.partitions = []
        start = Mbr.PARTITION_ENTRIES_START
        for i in range(0, Mbr.PARTITION_COUNT):
            end = start + Mbr.PARTITION_SIZE
            self.partitions.append(MbrPartition(data[start:end]))
            start = end

    def is_protected(self):
        return self.null == Mbr.PROTECTED

    def is_valid(self):
        return self.boot_signature == Mbr.BOOT_SIGNATURE_MBR

    def is_gpt(self):
        if not self.is_valid():
            return False

        for p in self.partitions:
            if p.is_type(MbrPartition.GPT_TYPE):
                return True

        return False

# vim: set ts=4 sw=4 tw=80:
