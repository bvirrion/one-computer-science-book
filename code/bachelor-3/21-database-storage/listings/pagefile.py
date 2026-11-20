"""pagefile.py -- a file of fixed-size pages, kept in memory, that counts every page
read and write: the unit of cost of everything in this chapter."""

PAGE = 4096


class PageFile:
    def __init__(self):
        self.pages, self.reads, self.writes = [], 0, 0

    def allocate(self):
        self.pages.append(bytes(PAGE))
        return len(self.pages) - 1  # the new page's number

    def read(self, pid):
        self.reads += 1
        return bytearray(self.pages[pid])

    def write(self, pid, data):
        assert len(data) == PAGE
        self.writes += 1
        self.pages[pid] = bytes(data)
