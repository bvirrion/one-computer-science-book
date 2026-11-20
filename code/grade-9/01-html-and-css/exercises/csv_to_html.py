import csv


def html_table(filename):
    """The rows of a CSV file as the text of an HTML table, header row in th cells."""
    with open(filename, encoding="utf-8") as f:
        rows = list(csv.reader(f))
    text = "<table>\n"
    for i in range(len(rows)):
        cell = "td"
        if i == 0:
            cell = "th"
        text = text + "  <tr>"
        for value in rows[i]:
            text = text + "<" + cell + ">" + value + "</" + cell + ">"
        text = text + "</tr>\n"
    return text + "</table>\n"
