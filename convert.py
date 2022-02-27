#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Reformat Awards Nominations Lists for Google Sheets

Input: sorted by category in a tab-separated file:

    Best Picture	Call Me By Your Name	Darkest Hour	Dunkirk	Get Out	Lady Bird	Phantom Thread	The Post	The Shape of Water	""\"Three Billboards Outside Ebbing, Missouri""\"
    Lead Actor	Timothée Chalamet, Call Me By Your Name	Daniel Day-Lewis, Phantom Thread	Daniel Kaluuya, Get Out	Gary Oldman, Darkest Hour	"Denzel Washington,""Roman J. Israel, Esq.""\"

Output (CSV):

    The Shape of Water, "Best Director (Guillermo del Toro), Best Picture, ..."

Upload this as a new document into Google Sheets and transfer the
columns into the shared sheet with the scorecard.

"""  # noqa

from operator import itemgetter
import csv
import logging

import click
from click_loglevel import LogLevel


@click.command()
@click.option("-l", "--level", type=LogLevel(), default=logging.ERROR)
@click.argument("src", type=click.File("r"))
@click.argument("dest", type=click.File("w"))
def main(level, src, dest):
    """Read SRC file and build DEST."""
    logging.basicConfig(format="[%(levelname)-8s] %(message)s", level=level)
    nominees = read_csv(src)
    write_csv(csv.writer(dest), nominees)


def restore_title(title):
    """Undo the title-sorted preparation.

    >>> restore_title('Jungle Book, The')
    'The Jungle Book'
    """
    words = title.split(" ")
    if words[-1] in ["A", "An", "The"]:
        words = [words[-1]] + words[0:-1]
        title = " ".join(words)
        title = title.rstrip(",")
    return title


def title_prep(title):
    """Prepare the title for title sorting (not on A, An, The).

    >>> title_prep('The Jungle Book')
    'Jungle Book, The'
    >>> title_prep('Another 48 Hrs.')
    'Another 48 Hrs.'
    """
    words = title.split(" ")
    if words[0] in ["A", "An", "The"]:
        title = "{}, {}".format(" ".join(words[1:]), words[0])
    return title


def read_csv(infile):
    """Read and parse the input CSV file."""
    reader = csv.reader(infile, delimiter="\t")
    result = {"short": {}, "feature": {}}

    for row in reader:
        category = row.pop(0)
        length = "short" if "Short" in category else "feature"
        nominees = list(csv.reader(row))
        logging.debug("%s: %s", category, nominees)
        for nominee in nominees:
            logging.debug("nominee: %s", nominee)
            film = nominee[-1]  # could be the only item
            if len(nominee) > 1:
                honoree = nominee[0]
                cat = f"{category} ({honoree})"
            else:
                cat = category

            film = title_prep(film)
            if film not in result[length]:
                result[length][film] = [cat]
            else:
                result[length][film] = sorted([*result[length][film], cat])

            logging.debug(
                "result[%s][%s] = %s", length, film, result[length][film]
            )

    return result


def multisort(xs, specs):
    """Sort by multiple factors; taken from the Python Sorting HOW TO."""
    for key, reverse in reversed(specs):
        xs.sort(key=itemgetter(key), reverse=reverse)
    return xs


def sort_shorts(nominees):
    """Sort the shorts by category."""
    categories = sorted(set([i[0] for i in nominees.values()]))
    result = []
    for category in categories:
        result.extend([k for k, v in nominees.items() if v[0] == category])
    logging.debug("sort_shorts() = %s", result)
    return result


def write_csv(writer, nominees):
    """Write the output CSV file."""
    # Add space for the headers
    writer.writerows([[None, None], [None, None], [None, None]])

    # assumes that shorts are only eligible for one category
    nom_counts = []
    for i in nominees["feature"]:
        nom_counts.append((i, len(nominees["feature"][i])))
    for film, _ in multisort(nom_counts, ((1, True), (0, False))):
        title = restore_title(film)
        writer.writerow([title, ", ".join(nominees["feature"][film])])

    # sort the shorts by category and name
    for film in sort_shorts(nominees["short"]):
        title = restore_title(film)
        writer.writerow([title, ", ".join(nominees["short"][film])])


if __name__ == "__main__":
    main()
