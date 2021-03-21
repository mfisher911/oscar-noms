Introduction
============

`prep-in.py` takes a list of nominations, sorted by category, pivots
them into a tab-separated file and makes slight formatting
improvements.

New for 2021, `get_nominations.py` builds the list that `prep-in.py`
could have produced by scraping Wikipedia.

`convert.py` transforms a tab-separated file from being row-ordered
to column-ordered, with collapsed keys, specifically trying to address
the problem of sorting out the most-nominated films and also separates
short films from feature-length films.


Usage
-----

    ./get_nominations.py --url https://en.wikipedia.org/wiki/93rd_Academy_Awards 2021-in.csv

This creates a CSV file that is similar to the "in-list.csv" file that
would have been produced by `prep-in.py` (so it can be directly fed to
`convert.py`).

    prep-in.py --in in-raw.txt --out in-list.csv
    
`in-raw.txt` is expected to be a file grouped by category with
the following structure:

    Best Picture
    Call Me By Your Name
    Darkest Hour
    Dunkirk
    ...
    
    Lead Actress
    Sally Hawkins, The Shape of Water
    Frances McDormand, "Three Billboards Outside Ebbing, Missouri"
    ...

    Original Song
    "I Can't Let You Throw Yourself Away", Toy Story 4
    "(I'm Gonna) Love Me Again", Rocketman

Note that "Original Song" is a magic phrase so that the song title is
included appropriately.

The output file should work nicely for `convert.py`.

    convert.py --in in-list.csv --out out-list.csv

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

    The Descendents,"Best Motion Picture, Best Actor (George Clooney)"
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

