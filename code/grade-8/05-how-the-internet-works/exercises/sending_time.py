def sending_time(size_bytes, rate):
    """Seconds to send size_bytes bytes at rate bits per second."""
    return size_bytes * 8 / rate
