#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Prepare Awards Nominations List for `convert.py`.

Input: sorted by category, categories separated by a blank line

    Lead Actor
    Timothée Chalamet, Call Me by Your Name
    Daniel Day-Lewis, Phantom Thread
    Daniel Kaluuya, Get Out
    Gary Oldman, Darkest Hour
    Denzel Washington, "Roman J. Israel, Esq."

Be sure to quote internal commas.

Output: collapsed and tidy, tab-separated

    Lead Actor	Timothée Chalamet,Call Me By Your Name	Daniel Day-Lewis,Phantom Thread	Daniel Kaluuya,Get Out	Gary Oldman,Darkest Hour	"Denzel Washington,""Roman J. Israel, Esq.""\"

"""

import argparse
import csv
import io
import re
import sys


def main():
    """ Control function. """
    args = parse_args()
    with open(args.infile, "r") as f:
        nominees = f.read()
    if args.outfile is None:
        writer = csv.writer(sys.stdout, delimiter="\t")
    else:
        writer = csv.writer(open(args.outfile, 'w'), delimiter="\t")
    write_csv(writer, nominees)


def parse_args():
    """ Grab the input / output filenames. """
    parser = argparse.ArgumentParser(
        description='Rotate the Award Nominee List')
    parser.add_argument('-i', '--in', dest='infile')
    parser.add_argument('-o', '--out', dest='outfile')
    return parser.parse_args()


def write_csv(writer, nominees):
    """ Write the output CSV file.

    NB: removes quoting from song titles
    """
    done = False
    while not done:
        end = nominees.find("\n\n")
        if end < 0:
            end = len(nominees) - 1
            done = True
        category = nominees[0:end]
        category = category.replace("’", "'")
        category = category.replace("“", '"')
        category = category.replace("”", '"')
        if category[0:category.find("\n")] == "Original Song":
            # Don't treat the song title differently from an
            # actor/director name
            category = category.replace('"', '')
        if ', ' in category:
            # All this stuff creates a StringIO object to collect the
            # CSV output in memory (vs using a file / temp file), and
            # then uses the CSV library to format it appropriately.
            # This could possibly be done more intelligently, but it
            # worked in 2018.
            output = io.StringIO()
            iwriter = csv.writer(output)
            for i in category.split("\n"):
                if re.search('^"', i):
                    # assumes the title is the only line element, such as:
                    #   "Three Billboards Outside Ebbing, Missouri"
                    # could fail if a nominated person is quoted
                    i = i.replace('"', '')
                    iwriter.writerow([i])
                else:
                    # This also assumes that the movie title is the
                    # part that has the commma.
                    vals = i.split(',', 1)
                    if len(vals) > 1:
                        vals[1] = vals[1].replace('"', '')
                    iwriter.writerow([j.strip() for j in vals])
            out = []
            for i in output.getvalue().split("\n"):
                if len(i) > 0:
                    out.append(i.strip())
            writer.writerow(out)
        else:
            writer.writerow(category.split("\n"))
        nominees = nominees[end + 2:]


if __name__ == "__main__":
    main()
