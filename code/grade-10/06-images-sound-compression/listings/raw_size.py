def raw_size(width, height, bytes_per_pixel=3):
    """Bytes of an uncompressed image: one value per colour per pixel."""
    return width * height * bytes_per_pixel


for width, height in ((640, 480), (1920, 1080), (4000, 3000)):
    size = raw_size(width, height)
    print(f"{width} x {height}: {width * height:>10,} pixels, {size:>10,} bytes"
          f" = {size / 2**20:.1f} MiB")
