#!/usr/bin/env python
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

from collections import defaultdict
import argparse
import csv
import sys


def main():
    """ Control function. """
    args = parse_args()
    nominees = defaultdict(list)
    read_csv(args.infile, nominees)
    features, shorts = separate_shorts(nominees)
    if args.outfile is None:
        writer = csv.writer(sys.stdout)
    else:
        writer = csv.writer(open(args.outfile, 'wb'))
    write_csv(writer, nominees, features, shorts)


def parse_args():
    """ Grab the input and output filenames. """
    parser = argparse.ArgumentParser(description=('Rotate the Award '
                                                  'Nominee List'))
    parser.add_argument('-i', '--in', dest='infile')
    parser.add_argument('-o', '--out', dest='outfile')
    return parser.parse_args()

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


def write_csv(writer, nominees, *runclasses):
    """ Write the output CSV file. """
    for runclass in runclasses:
        for film in sorted(runclass,
                           cmp=lambda x, y: cmp(len(nominees[y]),
                                                len(nominees[x]))
                           or cmp(x, y)):
            writer.writerow([title, ", ".join(sorted(nominees[film]))])
            title = restore_title(film)


if __name__ == "__main__":
    main()
