"""Grade 9, chapter 1: HTML and CSS, the pages and the tree programs."""

import importlib.util
import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
LISTINGS = HERE / "listings"
TOWN = HERE.parents[2] / "data" / "town"
sys.path.insert(0, str(LISTINGS))

from html_tree import show_tree, tags  # noqa: E402


def load(folder, name):
    spec = importlib.util.spec_from_file_location(name, HERE / folder / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


def quiet_tree(text):
    with redirect_stdout(io.StringIO()) as out:
        depth = show_tree(text)
    return depth, out.getvalue().splitlines()


def test_pages_are_well_formed():
    for path in [LISTINGS / "first_page.html", LISTINGS / "table.html",
                 LISTINGS / "weather_page.html", HERE / "exercises" / "my_page.html",
                 HERE / "exercises" / "places.html"]:
        assert quiet_tree(path.read_text())[0] == 0, path.name


def test_stats_and_list_pages(monkeypatch):
    monkeypatch.chdir(LISTINGS)
    stats = load("listings", "page_stats")
    for n in range(1, 30):
        assert stats.stats(stats.list_page(n)) == (n + 6, 4)
    assert stats.stats((LISTINGS / "weather_page.html").read_text()) == (14, 5)
    assert stats.stats((LISTINGS / "table.html").read_text()) == (10, 3)


def test_exercises(tmp_path):
    depth, lines = quiet_tree('<ul><li><a href="x.html">x</a></li><li>y</li></ul>')
    assert (depth, lines) == (0, ["ul", "  li", "    a", "  li"])
    wrong = quiet_tree("<p>An <em>important</p></em> day")
    assert wrong[0] == 0
    first = (LISTINGS / "first_page.html").read_text()
    assert load("exercises", "links").links(first) == ["books.html"]
    assert 'alt="' in [t for t in tags(first) if t.startswith("img")][0]
    assert 300 + 2 * 10 + 2 * 2 == 324
    table = load("exercises", "csv_to_html").html_table(TOWN / "places.csv")
    assert table.startswith("<table>\n  <tr><th>place_id</th>")
    assert quiet_tree(table)[0] == 0
    assert table.count("<tr>") == len((TOWN / "places.csv").read_text().splitlines())
