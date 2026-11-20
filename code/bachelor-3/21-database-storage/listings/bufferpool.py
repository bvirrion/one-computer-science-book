"""bufferpool.py -- a buffer pool: a fixed number of frames caching pages of a PageFile.
A fetched page is pinned until unpinned; a page changed in a frame is dirty and is
written back when its frame is reused. Victims are chosen by the clock algorithm."""


class BufferPool:
    def __init__(self, pagefile, frames):
        self.file, self.n = pagefile, frames
        self.page = [None] * frames  # the page number held by each frame
        self.data = [None] * frames
        self.pins = [0] * frames  # pin count of each frame
        self.dirty = [False] * frames
        self.ref = [False] * frames  # the clock's reference bits
        self.where, self.hand, self.hits, self.misses = {}, 0, 0, 0

    def fetch(self, pid):
        if pid in self.where:
            self.hits += 1
            f = self.where[pid]
        else:
            self.misses += 1
            f = self.victim()
            if self.page[f] is not None:
                if self.dirty[f]:
                    self.file.write(self.page[f], self.data[f])
                del self.where[self.page[f]]
            self.page[f], self.data[f], self.dirty[f] = pid, self.file.read(pid), False
            self.where[pid] = f
        self.pins[f] += 1
        self.ref[f] = True
        return self.data[f]

    def unpin(self, pid, dirty=False):
        f = self.where[pid]
        self.pins[f] -= 1
        self.dirty[f] |= dirty

    def victim(self):
        """Clock: sweep the frames, clearing reference bits, until an unpinned frame
        whose bit is already clear; a frame never used is taken at once."""
        for _ in range(2 * self.n + 1):
            f, self.hand = self.hand, (self.hand + 1) % self.n
            if self.page[f] is None:
                return f
            if self.pins[f] == 0:
                if not self.ref[f]:
                    return f
                self.ref[f] = False
        raise RuntimeError("every frame is pinned")

    def flush(self):
        for f in range(self.n):
            if self.page[f] is not None and self.dirty[f]:
                self.file.write(self.page[f], self.data[f])
                self.dirty[f] = False
