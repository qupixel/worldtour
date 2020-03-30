import reader as r
from analyzer import Analyzer
import numpy as np
import pandas as pd

FILE = "data/book.txt"


def test_reader():
    """Test basic properties of BookReader."""
    book = r.BookReader(FILE, start_term="Chapter I")
    assert book._lines[0] == "Chapter I\n"

    book = r.BookReader(FILE)
    assert "The Project Gutenberg" in book._lines[0]

    locs = book.detect_item("Chapter XXXIII")
    assert int(np.sum(locs)) == 1

    book._parse_chapters()
    assert len(book._chapters) == 37

    book = r.BookReader(FILE, end_term="Last updated")
    assert book._lines[-1].startswith("Release Date")

    places = book.find_places("This is the city of London")
    assert len(places) == 1
    assert places[0] == "London"

    places = book.find_places(
        "We arrived to Calcutta City",
        replace_dict={"Calcutta City": "Kolkata"},
        )
    assert len(places) == 1
    assert places[0] == "Kolkata"

    places = book.find_places(
        "Holland is a place",
        ignore_list=["Holland"],
        )
    assert len(places) == 0


def test_analyzer():
    """Test basic analyzer."""
    analyzer = Analyzer("data/worldcities.csv")
    frm_qry = pd.DataFrame(pd.Series(["Grenoble"]), columns=["place"])
    aux = analyzer.query(frm_qry)
    assert aux[0].shape[0] == 1

    orig_shape = analyzer.df.shape[0]
    analyzer.resolve([["Paris", "country", "France"]])
    assert analyzer.df.shape[0] + 4 == orig_shape

    aux = analyzer.query(["Barcelonia"])
    assert aux[0].shape[0] == 0

    aux = analyzer.query("Grenoble")
    assert aux[0].shape[0] == 1
    idx = analyzer.df.city == "San Francisco"
    assert int(analyzer.df.lng_srt[idx].values[1]) == 237
