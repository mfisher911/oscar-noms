#!/usr/bin/env python

import csv
import io
import logging
from datetime import date

import click
import httpx
from bs4 import BeautifulSoup
from click_loglevel import LogLevel


def clean(cat):
    """Clean a category's nominees to only return needed info

    Some things are movie title only, some things have a person and a
    movie title, and the Best Original Song only keeps the song name
    and movie title.
    """
    # title only:
    title_only = [
        "Best Picture",
        "Best Original Screenplay",
        "Best Adapted Screenplay",
        "Best International Feature Film",
        "Best Cinematography",
        "Best Costume Design",
        "Best Production Design",
        "Best Makeup and Hairstyling",
        "Best Sound",
        "Best Original Score",
        "Best Film Editing",
        "Best Visual Effects",
        "Best Animated Feature Film",
        "Best Animated Short Film",
        "Best Documentary Feature",
        "Best Documentary Short Subject",
        "Best Live Action Short Film",
    ]
    subject_title = [
        "Best Director",
        "Best Actor",
        "Best Actress",
        "Best Supporting Actor",
        "Best Supporting Actress",
    ]
    best_song = ["Best Original Song"]
    award = cat.select("div")[0].text
    logging.debug("%s", award)
    result = {"award": simplify(award), "nominees": []}
    if award in title_only:
        for nominee in cat.select("ul li"):
            # need to get the part after the dash
            try:
                title = nominee.select("a")[0].text
            except IndexError:
                logging.info("No <a> for %s", title)
                title = nominee.text
            result["nominees"].append(title)
            logging.debug("    %s", title)
    elif award in subject_title:
        for nominee in cat.select("ul li"):
            # need before and after dash
            subject, title = nominee.select("a")[0:2]
            nomination = (
                subject.text,
                title.text,
            )
            result["nominees"].append(nomination)
            logging.debug("    %s", nomination)
    elif award in best_song:
        for nominee in cat.select("ul li"):
            # "song title" from Movie -- text
            subject, title = (
                nominee.text[0 : nominee.text.find("–") - 1]
                .replace('"', "")
                .split(" from ")
            )
            nomination = (
                subject,
                title,
            )
            result["nominees"].append(nomination)
            logging.debug("    %s", nomination)
    else:
        raise ValueError("Not sure how to handle %s", award)

    return result


def simplify(nomination):
    """Shorten some of the award titles for spreadsheet presentation"""
    remap = {
        "Best Makeup and Hairstyling": "Best Makeup",
        "Best Film Editing": "Best Editing",
        "Best Animated Feature Film": "Best Animated Feature",
        "Best Animated Short Film": "Best Animated Short",
        "Best Documentary Feature": "Best Documentary",
        "Best Documentary Short Subject": "Best Short Documentary",
        "Best Live Action Short Film": "Best Live Short",
        "Best Supporting Actor": "Supporting Actor",
        "Best Supporting Actress": "Supporting Actress",
    }
    return remap[nomination] if nomination in remap else nomination


@click.command()
@click.option("-l", "--level", type=LogLevel(), default=logging.ERROR)
@click.option("--url", help="Wikipedia URL")
@click.argument("dest", type=click.File("w"))
def main(level, url, dest):
    """Create DEST.

    DEST is a file that can be used as input for convert.py. It will
    have one line per category and be tab-separated, with quoted/CSV
    internal fields where appropriate (for instance:

    Supporting Actor        Sacha Baron Cohen,The Trial of the Chicago 7

    """
    logging.basicConfig(format="[%(levelname)-8s] %(message)s", level=level)
    if not url:
        year = date.today().year
        print(
            f"Get the Wikipedia link:\n"
            f"<https://en.wikipedia.org/wiki/Special:Search?search={year}%20academy%20award%20nominations&go=Go&ns0=1>"  # noqa
        )
        url = input("> ")

    r = httpx.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    # get to nominations table
    awards = soup.find_all("table", class_="wikitable")[0]

    writer = csv.writer(dest, delimiter="\t")
    for nom in awards.select("tbody tr td"):
        data = clean(nom)
        nomlist = []
        for i in data["nominees"]:
            mem_file = io.StringIO()
            mem_writer = csv.writer(mem_file)
            if type(i) is tuple:
                mem_writer.writerow(i)
            else:
                mem_writer.writerow([i])
            nomlist.append(mem_file.getvalue().strip())
        writer.writerow([data["award"], *nomlist])


if __name__ == "__main__":
    main()
