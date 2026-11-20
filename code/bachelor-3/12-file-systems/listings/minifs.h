/* minifs.h -- a small Unix-like file system in an image file of 1024 blocks of 1 KiB. */
#include <stdint.h>

#define BSIZE 1024
#define NBLOCKS 1024
#define NINODES 128
#define NDIRECT 10
#define NPTRS (BSIZE / 4)              /* block numbers in an indirect block: 256 */
#define NAMELEN 28
#define ROOT 1                         /* inode 0 is never used */

enum { SUPER = 0, IBITMAP = 1, BBITMAP = 2, ITABLE = 3, ITABLE_BLOCKS = 8,
       JOURNAL = 11, JOURNAL_BLOCKS = 32, DATA = 43 };
enum { T_FREE, T_FILE, T_DIR };

struct inode {                         /* 64 bytes: 16 per block */
    uint16_t type, nlink;
    uint32_t size;
    uint32_t direct[NDIRECT];
    uint32_t indirect, dindirect;      /* dindirect: exercise 6 */
    uint32_t unused[2];
};
struct dirent { uint32_t ino; char name[NAMELEN]; };   /* 32 bytes: 32 per block */

extern long reads, writes;             /* blocks read and written so far */
extern long crash_at;                  /* if > 0, every write after that many is lost */
extern int journaling, replayed;      /* replayed: the last mount replayed the journal */
extern int show_writes;                /* print each block written */

void mkfs(const char *path);
void fs_mount(const char *path);       /* opens the image and replays the journal */
void fs_unmount(void);
struct inode fs_stat(int ino);
int fs_lookup(int dir, const char *name);
int fs_create(int dir, const char *name, int type);
long fs_write(int ino, uint32_t off, const void *buf, uint32_t n);
long fs_read(int ino, uint32_t off, void *buf, uint32_t n);
int fs_unlink(int dir, const char *name);
void fs_ls(int dir, const char *path);
int fs_check(int verbose);             /* the inconsistencies (printed if verbose) */
