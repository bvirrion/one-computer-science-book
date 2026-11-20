/* ex5_unlink_bug.c -- exercise 5: unlink as first written. */
static int unlink_bug(int dir, const char *name)
{
    struct dirent e;
    for (uint32_t off = 0; fs_read(dir, off, &e, sizeof e) == sizeof e; off += sizeof e) {
        if (!e.ino || strcmp(e.name, name) != 0) continue;
        tx_begin();
        struct inode in, d = iget(dir);
        uint32_t ino = e.ino;
        memset(&e, 0, sizeof e);
        iwrite(dir, &d, off, (uint8_t *)&e, sizeof e);
        memset(&in, 0, sizeof in);
        iput(ino, &in);
        set_bit(IBITMAP, ino, 0);
        tx_commit();
        return 0;
    }
    return -1;
}
