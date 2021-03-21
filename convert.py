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

"""

from operator import itemgetter
import csv
import logging

import click
from click_loglevel import LogLevel


def restore_title(title):
    """Undo the title-sorted preparation.

def separate_shorts(nominees):
    """ Separate the shorts from the features. """
    features = set()
    shorts = set()
    for film in nominees.keys():
        if any("Short" in i for i in nominees[film]):
            shorts.add(film)
        else:
            features.add(film)

    if (features | shorts) != set(nominees.keys()):
        print "Warning: the following films were missed:\n{}"\
            .format(list(set(nominees.keys()) - (features | shorts)))

    return features, shorts
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


def read_csv(infile, nominees):
    """ Read and parse the input CSV file. """
    reader = csv.reader(open(infile), delimiter="\t")
    for row in reader:
        category = row.pop(0)
        choices = csv.reader(row)
        for nominee in choices:
            if len(nominee) > 1:
                honoree = nominee[0]
                film = nominee[1]
                if category == "Original Song":
                    honoree = '"{}"'.format(honoree)
                cat = "{category} ({honoree})".format(category=category,
                                                      honoree=honoree)
            else:
                film = nominee[0]
                cat = category
            film = title_prep(film)
            nominees[film].append(cat)


def multisort(xs, specs):
    for key, reverse in reversed(specs):
        xs.sort(key=itemgetter(key), reverse=reverse)
    return xs


def write_csv(writer, nominees):
    """ Write the output CSV file. """
    # Add space for the headers
    writer.writerows([[None, None], [None, None], [None, None]])

    for runclass in ["feature", "short"]:
        nom_count = []
        for i in nominees[runclass]:
            nom_count.append((i, len(nominees[runclass][i])))
        for film, _ in multisort(nom_count, ((1, True), (0, False))):
            title = restore_title(film)
            writer.writerow([title, ", ".join(nominees[runclass][film])])


if __name__ == "__main__":
    main()
