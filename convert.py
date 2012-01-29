#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Reformat the Academy Awards Nominations List.

Input: sorted by category in a CSV file:

Best Motion Picture	The Artist	The Descendents
Best Actor	Demián Bichir, A Better Life	George Clooney, The Descendents

Output (CSV):

A Better Life	Best Actor (Demián Bichir)
The Artist	Best Motion Picture
The Descendents	Best Motion Picture	Best Actor (George Clooney)

"""


import argparse
import csv


def main():
    """ Control function. """
    args = parse_args()
    nominees = {}
    read_csv(args.infile, nominees)
    write_csv(args.outfile, nominees)


def parse_args():
    """ Grab the input and output filenames. """
    parser = argparse.ArgumentParser(description='Rotate the Oscar List')
    parser.add_argument('-i', '--in', dest='infile')
    parser.add_argument('-o', '--out', dest='outfile')
    return parser.parse_args()


def de_title(title):
    """ Undo the title-sorted preparation. """
    words = title.split(' ')
    if words[-1] in ['A', 'An', 'The']:
        words = [words[-1]] + words[0:-1]
        title = " ".join(words)
        title = title.rstrip(',')
    return title


def title_prep(title):
    """ Prepare the title for title sorting (not on A, An, The). """
    words = title.split(' ')
    if words[0] in ['A', 'An', 'The']:
        title = "{}, {}".format(" ".join(words[1:]), words[0])
    return title


def read_csv(infile, nominees):
    """ Read and parse the input CSV file. """
    reader = csv.reader(open(infile))
    for row in reader:
        category = row.pop(0)
        for nominee in row:
            cat = category
            film = nominee
            specific = None
            if "," in nominee:
                specific, film = nominee.split(', ')
            if " " in film:
                film = title_prep(film)
            if specific:
                cat = "{category} ({specific})".format(category=category,
                                                       specific=specific)
            if film in nominees:
                nominees[film].append(cat)
            else:
                nominees[film] = [cat]


def write_csv(outfile, nominees):
    """ Write the output CSV file. """
    writer = csv.writer(open(outfile, 'wb'))
    for film in sorted(nominees.keys(),
                       cmp=lambda x, y: cmp(len(nominees[y]),
                                            len(nominees[x])) \
                           or cmp(x, y)):
        title = de_title(film)
        writer.writerow([title, ", ".join(sorted(nominees[film]))])


if __name__ == "__main__":
    main()
