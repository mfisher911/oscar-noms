Introduction
============

New for 2021, `get_nominations.py` builds the list of category
nominations by scraping Wikipedia.

`convert.py` transforms a tab-separated file from being row-ordered
to column-ordered, with collapsed keys, specifically trying to address
the problem of sorting out the most-nominated films and also separates
short films from feature-length films.


Usage
-----

    ./get_nominations.py \
        --url https://en.wikipedia.org/wiki/93rd_Academy_Awards \
        $(date '+%Y-in.csv')

This creates a CSV file that can be directly fed to `convert.py`.

    ./convert.py in-list.csv out-list.csv

`in-list.csv` is expected to be a tab-separated file with the following
structure:

    Category 1	Title 1	Title 2	...
    Category 2	"Person 1, Title 1"	"Person 2, Title 2"	...

Note that the "Person 1, Title 1" (such as: George Clooney, The
Descendents) includes a comma. It's expected that a CSV-generating
tool will properly escape (quote) the output.


Output
------

`convert.py` will output to standard output if an output file is not
specified.

Given the sample input:

    Best Motion Picture	The Artist	The Descendents
    Best Actor	"Demián Bichir, A Better Life"	"George Clooney, The Descendents"

The output will be similar to:

    The Descendents,"Best Actor (George Clooney), Best Motion Picture"
    The Artist,Best Motion Picture
    A Better Life,Best Actor (Demián Bichir)

It will be sorted by count of nominations (most to least) and then by
title. The nominated categories are sorted alphabetically (some are
abbreviated).

This output can be imported into (for instance) a Google Spreadsheet.


Copyright
---------

Oscar (R) and Academy Awards (R) are registered trademarks of the
Academy of Motion Picture Arts and Sciences (R). Use in this project
title does not indicate a relationship with the above entities.

