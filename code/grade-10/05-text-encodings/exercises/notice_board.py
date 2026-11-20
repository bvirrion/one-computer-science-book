"""Problem: the notice board of the Lighthouse Cafe."""
import town

MESSAGE = "Lighthouse Café: crêpes today"


def garble(text, layers):
    """Encode text as UTF-8 and read the bytes back as Latin-1, `layers` times."""
    for _ in range(layers):
        text = text.encode("utf-8").decode("latin-1")
    return text


def ungarble(text, layers):
    for _ in range(layers):
        text = text.encode("latin-1").decode("utf-8")
    return text


def name_sizes():
    names = [place["name"] for place in town.load("places")]
    encodings = ("utf-8", "utf-16-le", "latin-1")
    return {enc: sum(len(n.encode(enc)) for n in names) for enc in encodings}


if __name__ == "__main__":
    dump = MESSAGE.encode("utf-8")
    for start in range(0, len(dump), 16):
        print(dump[start:start + 16].hex(" "))
    for layers in (1, 2):
        print(layers, ascii(garble(MESSAGE, layers)))
    sizes = name_sizes()
    print(sizes, "saved:", sizes["utf-16-le"] - sizes["utf-8"])
