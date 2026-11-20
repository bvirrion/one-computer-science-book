"""slotted.py -- a slotted page: a 4-byte header (slot count, start of the records), a
slot array growing from the front, records growing from the back, free space between.
A record identifier is (page number, slot number); a slot of length 0 is empty."""

import struct

from pagefile import PAGE

HEADER = struct.Struct("<HH")  # slot count, start of the records
SLOT = struct.Struct("<HH")  # offset and length of one record


class SlottedPage:
    def __init__(self, data=None):
        self.data = bytearray(data) if data else bytearray(PAGE)
        if data is None:
            HEADER.pack_into(self.data, 0, 0, PAGE)

    def header(self):
        return HEADER.unpack_from(self.data, 0)

    def slot(self, i):
        return SLOT.unpack_from(self.data, HEADER.size + i * SLOT.size)

    def free_space(self):
        count, start = self.header()
        return start - (HEADER.size + count * SLOT.size)

    def insert(self, record):
        count, start = self.header()
        empty = [i for i in range(count) if self.slot(i)[1] == 0]
        need = len(record) + (0 if empty else SLOT.size)
        if need > self.free_space():
            return None  # the page is full
        start -= len(record)
        self.data[start : start + len(record)] = record
        i = empty[0] if empty else count
        SLOT.pack_into(self.data, HEADER.size + i * SLOT.size, start, len(record))
        HEADER.pack_into(self.data, 0, max(count, i + 1), start)
        return i

    def get(self, i):
        offset, length = self.slot(i)
        return bytes(self.data[offset : offset + length]) if length else None

    def delete(self, i):
        SLOT.pack_into(self.data, HEADER.size + i * SLOT.size, 0, 0)

    def compact(self):
        """Slide the live records to the back of the page; slot numbers do not change,
        so record identifiers stay valid."""
        count, _ = self.header()
        records = [(i, self.get(i)) for i in range(count)]
        start = PAGE
        for i, rec in records:
            if rec:
                start -= len(rec)
                self.data[start : start + len(rec)] = rec
                SLOT.pack_into(self.data, HEADER.size + i * SLOT.size, start, len(rec))
        HEADER.pack_into(self.data, 0, count, start)
