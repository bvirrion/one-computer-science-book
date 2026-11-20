/* minifs.c -- superblock, bitmaps, inode table, direct and indirect blocks, directories
   as files, and an optional write-ahead journal. One block of the image per access. */
#include <stdio.h>
#include <string.h>
#include "minifs.h"

long reads, writes, crash_at;
int journaling, replayed, show_writes;
static FILE *disk;

/* ---- the disk: one block per call; a crash loses every later write ---- */
static void disk_read(uint32_t b, void *buf)
{
    fseek(disk, (long)b * BSIZE, SEEK_SET);
    if (fread(buf, BSIZE, 1, disk) != 1) memset(buf, 0, BSIZE);
    reads++;
}

static void disk_write(uint32_t b, const void *buf)
{
    if (crash_at && writes >= crash_at) return;        /* the machine has stopped */
    fseek(disk, (long)b * BSIZE, SEEK_SET);
    fwrite(buf, BSIZE, 1, disk);
    if (show_writes) printf(" %u", b);
    writes++;
}

/* ---- the journal: an operation's writes are held, logged, committed, then applied ---- */
#define COMMIT 0x434f4d4du
static struct { uint32_t block; uint8_t data[BSIZE]; } tx[JOURNAL_BLOCKS - 1];
static int ntx, in_tx;

static void get(uint32_t b, void *buf)                 /* as the operation sees it */
{
    for (int i = 0; i < ntx; i++)
        if (tx[i].block == b) { memcpy(buf, tx[i].data, BSIZE); return; }
    disk_read(b, buf);
}

static void put(uint32_t b, const void *buf)
{
    if (!in_tx) { disk_write(b, buf); return; }
    int i = 0;
    while (i < ntx && tx[i].block != b) i++;
    if (i == ntx) tx[ntx++].block = b;
    memcpy(tx[i].data, buf, BSIZE);
}

static void tx_begin(void) { in_tx = journaling; ntx = 0; }

static void tx_commit(void)
{
    if (!in_tx) return;
    uint32_t desc[NPTRS] = {0};
    for (int i = 0; i < ntx; i++) {                    /* 1. log the new blocks */
        disk_write(JOURNAL + 1 + i, tx[i].data);
        desc[2 + i] = tx[i].block;                     /* and where each belongs */
    }
    desc[0] = COMMIT, desc[1] = ntx;
    disk_write(JOURNAL, desc);                         /* 2. commit: one block write */
    for (int i = 0; i < ntx; i++)                      /* 3. checkpoint: write in place */
        disk_write(tx[i].block, tx[i].data);
    memset(desc, 0, sizeof desc);
    disk_write(JOURNAL, desc);                         /* 4. the journal is empty again */
    in_tx = ntx = 0;
}

static void replay(void)                               /* at mount, after a crash */
{
    uint32_t desc[NPTRS];
    uint8_t data[BSIZE];
    disk_read(JOURNAL, desc);
    replayed = desc[0] == COMMIT;
    if (!replayed) return;                             /* nothing committed: ignore */
    for (uint32_t i = 0; i < desc[1]; i++) {
        disk_read(JOURNAL + 1 + i, data);
        disk_write(desc[2 + i], data);
    }
    memset(desc, 0, sizeof desc);
    disk_write(JOURNAL, desc);
}

/* ---- inodes and bitmaps ---- */
static struct inode iget(int ino)
{
    uint8_t b[BSIZE];
    struct inode in;
    get(ITABLE + ino / 16, b);
    memcpy(&in, b + ino % 16 * 64, sizeof in);
    return in;
}

static void iput(int ino, const struct inode *in)
{
    uint8_t b[BSIZE];
    get(ITABLE + ino / 16, b);
    memcpy(b + ino % 16 * 64, in, sizeof *in);
    put(ITABLE + ino / 16, b);
}

static int bit(uint32_t bitmap, int i)
{
    uint8_t b[BSIZE];
    get(bitmap, b);
    return b[i / 8] >> i % 8 & 1;
}

static void set_bit(uint32_t bitmap, int i, int on)
{
    uint8_t b[BSIZE];
    get(bitmap, b);
    b[i / 8] = on ? b[i / 8] | 1 << i % 8 : b[i / 8] & ~(1 << i % 8);
    put(bitmap, b);
}

static int alloc_bit(uint32_t bitmap, int from, int n)
{
    for (int i = from; i < n; i++)
        if (!bit(bitmap, i)) { set_bit(bitmap, i, 1); return i; }
    return 0;                                          /* none free */
}

static uint32_t new_block(int zero)
{
    uint32_t b = alloc_bit(BBITMAP, DATA, NBLOCKS);
    uint8_t z[BSIZE] = {0};
    if (b && zero) put(b, z);                          /* an indirect block starts empty */
    return b;
}

/* ---- the file's k-th block: direct, then through the indirect block ---- */
#ifdef DOUBLE_INDIRECT
static uint32_t bmap_double(struct inode *in, uint32_t k, int *fresh);
#endif

static uint32_t bmap(struct inode *in, uint32_t k, int *fresh)  /* fresh: allocate */
{
    if (k < NDIRECT) {
        if (!in->direct[k] && fresh) *fresh = 1, in->direct[k] = new_block(0);
        return in->direct[k];
    }
    k -= NDIRECT;
    if (k < NPTRS) {
        if (!in->indirect && !fresh) return 0;
        if (!in->indirect && !(in->indirect = new_block(1))) return 0;
        uint32_t p[NPTRS];
        get(in->indirect, p);
        if (!p[k] && fresh && (p[k] = new_block(0))) *fresh = 1, put(in->indirect, p);
        return p[k];
    }
#ifdef DOUBLE_INDIRECT
    return bmap_double(in, k - NPTRS, fresh);
#else
    return 0;                                          /* beyond the largest file */
#endif
}

/* ---- reading and writing bytes ---- */
static long iwrite(int ino, struct inode *in, uint32_t off, const uint8_t *buf, uint32_t n)
{
    uint8_t b[BSIZE];
    uint32_t done = 0;
    while (done < n) {
        uint32_t at = (off + done) % BSIZE, len = BSIZE - at;
        if (len > n - done) len = n - done;
        int fresh = 0;
        uint32_t blk = bmap(in, (off + done) / BSIZE, &fresh);
        if (!blk) break;                               /* disk full, or file too large */
        if (fresh) memset(b, 0, BSIZE); else get(blk, b);
        memcpy(b + at, buf + done, len);
        put(blk, b);                                   /* the data block */
        done += len;
    }
    if (off + done > in->size) in->size = off + done;
    iput(ino, in);                                     /* then the inode: size, pointers */
    return done;
}

long fs_write(int ino, uint32_t off, const void *buf, uint32_t n)
{
    tx_begin();
    struct inode in = iget(ino);
    long done = iwrite(ino, &in, off, buf, n);
    tx_commit();
    return done;
}

long fs_read(int ino, uint32_t off, void *buf, uint32_t n)
{
    struct inode in = iget(ino);
    uint8_t b[BSIZE];
    if (off >= in.size) return 0;
    if (n > in.size - off) n = in.size - off;
    for (uint32_t done = 0; done < n;) {
        uint32_t at = (off + done) % BSIZE, len = BSIZE - at;
        if (len > n - done) len = n - done;
        uint32_t blk = bmap(&in, (off + done) / BSIZE, NULL);
        if (blk) get(blk, b); else memset(b, 0, BSIZE);
        memcpy((uint8_t *)buf + done, b + at, len);
        done += len;
    }
    return n;
}

/* ---- directories: files of 32-byte entries ---- */
int fs_lookup(int dir, const char *name)
{
    struct dirent e;
    for (uint32_t off = 0; fs_read(dir, off, &e, sizeof e) == sizeof e; off += sizeof e)
        if (e.ino && strcmp(e.name, name) == 0) return e.ino;
    return 0;
}

int fs_create(int dir, const char *name, int type)
{
    if (fs_lookup(dir, name)) return 0;
    tx_begin();
    int ino = alloc_bit(IBITMAP, ROOT + 1, NINODES);   /* 1. the inode bitmap */
    if (!ino) return 0;
    struct inode in = {.type = type, .nlink = 1};
    iput(ino, &in);                                    /* 2. the inode */
    struct dirent e = {.ino = ino};
    strncpy(e.name, name, NAMELEN - 1);
    struct inode d = iget(dir);
    iwrite(dir, &d, d.size, (uint8_t *)&e, sizeof e);  /* 3. the entry, 4. the size */
    tx_commit();
    return ino;
}

static void free_blocks(struct inode *in)
{
    for (int k = 0; k < NDIRECT; k++)
        if (in->direct[k]) set_bit(BBITMAP, in->direct[k], 0);
    if (in->indirect) {
        uint32_t p[NPTRS];
        get(in->indirect, p);
        for (int k = 0; k < NPTRS; k++)
            if (p[k]) set_bit(BBITMAP, p[k], 0);
        set_bit(BBITMAP, in->indirect, 0);
    }
}

int fs_unlink(int dir, const char *name)
{
    struct dirent e;
    for (uint32_t off = 0; fs_read(dir, off, &e, sizeof e) == sizeof e; off += sizeof e) {
        if (!e.ino || strcmp(e.name, name) != 0) continue;
        tx_begin();
        struct inode in = iget(e.ino), d = iget(dir);
        uint32_t ino = e.ino;
        memset(&e, 0, sizeof e);
        iwrite(dir, &d, off, (uint8_t *)&e, sizeof e);  /* the entry is cleared */
        free_blocks(&in);                              /* the file's blocks */
        memset(&in, 0, sizeof in);
        iput(ino, &in);
        set_bit(IBITMAP, ino, 0);                      /* and its inode */
        tx_commit();
        return 0;
    }
    return -1;
}

/* ---- creating, mounting, listing ---- */
void mkfs(const char *path)
{
    uint8_t zero[BSIZE] = {0};
    disk = fopen(path, "w+b");
    for (int b = 0; b < NBLOCKS; b++) disk_write(b, zero);
    uint32_t super[NPTRS] = {0x4d494e49u, NBLOCKS, NINODES, IBITMAP, BBITMAP,
                             ITABLE, ITABLE_BLOCKS, JOURNAL, JOURNAL_BLOCKS, DATA};
    disk_write(SUPER, super);
    for (int b = 0; b < DATA; b++) set_bit(BBITMAP, b, 1);   /* the metadata's blocks */
    set_bit(IBITMAP, 0, 1);
    set_bit(IBITMAP, ROOT, 1);
    struct inode root = {.type = T_DIR, .nlink = 1};
    iput(ROOT, &root);
    fclose(disk);
    reads = writes = 0;
}

void fs_mount(const char *path)
{
    disk = fopen(path, "r+b");
    replay();
}

void fs_unmount(void) { fclose(disk); }

struct inode fs_stat(int ino) { return iget(ino); }

void fs_ls(int dir, const char *path)
{
    struct dirent e;
    for (uint32_t off = 0; fs_read(dir, off, &e, sizeof e) == sizeof e; off += sizeof e) {
        if (!e.ino) continue;
        struct inode in = iget(e.ino);
        char full[64];
        snprintf(full, sizeof full, "%s%s", path, e.name);
        printf("%-12s inode %u  %-4s %5u bytes  blocks", full, e.ino,
               in.type == T_DIR ? "dir" : "file", in.size);
        for (int k = 0; k < NDIRECT && in.direct[k]; k++) printf(" %u", in.direct[k]);
        if (in.indirect) {
            uint32_t p[NPTRS];
            get(in.indirect, p);
            printf(" | indirect %u:", in.indirect);
            for (int k = 0; k < NPTRS && p[k]; k++) printf(" %u", p[k]);
        }
        printf("\n");
    }
}

/* ---- the checker: what the bitmaps say against what the directory tree uses ---- */
static uint8_t used_block[NBLOCKS], used_inode[NINODES];
static int problems, verbose_check;

#define report(...) (problems++, verbose_check && printf(__VA_ARGS__))

static void claim(uint32_t b, int ino)
{
    if (used_block[b]++) report("  block %u used twice (inode %d)\n", b, ino);
}

static void walk(int ino)
{
    struct inode in = iget(ino);
    if (used_inode[ino]++) return;
    if (in.type == T_FREE) {
        report("  inode %d is in a directory but free\n", ino);
        return;
    }
    for (int k = 0; k < NDIRECT; k++)
        if (in.direct[k]) claim(in.direct[k], ino);
    if (in.indirect) {
        uint32_t p[NPTRS];
        claim(in.indirect, ino);
        get(in.indirect, p);
        for (int k = 0; k < NPTRS; k++)
            if (p[k]) claim(p[k], ino);
    }
    struct dirent e;
    if (in.type == T_DIR)
        for (uint32_t off = 0; fs_read(ino, off, &e, sizeof e) == sizeof e; off += sizeof e)
            if (e.ino) walk(e.ino);
}

int fs_check(int verbose)
{
    memset(used_block, 0, sizeof used_block);
    memset(used_inode, 0, sizeof used_inode);
    problems = 0;
    verbose_check = verbose;
    walk(ROOT);
    for (int i = ROOT + 1; i < NINODES; i++)
        if (bit(IBITMAP, i) && !used_inode[i])
            report("  inode %d allocated but in no directory\n", i);
        else if (!bit(IBITMAP, i) && used_inode[i])
            report("  inode %d in use but free in the bitmap\n", i);
    for (int b = DATA; b < NBLOCKS; b++)
        if (bit(BBITMAP, b) && !used_block[b])
            report("  block %d allocated but used by no file (a leak)\n", b);
        else if (!bit(BBITMAP, b) && used_block[b])
            report("  block %d in use but free in the bitmap\n", b);
    return problems;
}
