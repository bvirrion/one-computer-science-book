"""Exercise 11: the duration of a WAV file, from its header."""
import wave


def wav_duration(path):
    """Return the duration in seconds of the WAV file at path."""
    with wave.open(str(path), "rb") as w:
        return w.getnframes() / w.getframerate()
