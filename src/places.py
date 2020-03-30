"""Extract the cities mentioned in an ebook."""


from reader import BookReader
from analyzer import Analyzer

import json
import pandas as pd
import numpy as np
from tqdm import tqdm


def main():
    """Run main function."""
    ST = "Chapter I"
    ET = "End of Project"
    BOOK = "data/book.txt"
    CONFIG = "data/around.json"
    CITIES = "data/worldcities.csv"
    OUTPUT = "cities.csv"

    reader = BookReader(BOOK, start_term=ST, end_term=ET)
    with open(CONFIG) as f:
        config = json.load(f)

    reader._parse_chapters()

    all_places = []
    for i, c in enumerate(tqdm(reader._chapters)):
        s = " ".join(c).replace("\n", "")
        places = reader.find_places(
            s,
            replace_dict=config['replace'],
            ignore_list=config['ignore'])
        n = len(places)
        all_places += zip([i]*n, places)

    print("***Selected places***")
    places = pd.DataFrame(all_places, columns=["chapter", "place"])
    places['occ'] = 1
    selected_places = places.groupby("place").agg(
        {'occ': 'sum', 'chapter': 'median'}
        )[['occ', 'chapter']].reset_index()

    # Append manual places
    df_append = pd.DataFrame(pd.Series(config["add"]), columns=["place"])
    df_append['occ'] = 0
    df_append['chapter'] = 0
    selected_places = selected_places.append(df_append, ignore_index=True)
    print(selected_places)

    print("Selected places:", selected_places.shape)
    print("***")

    selected_places['img'] = None
    selected_places['word_occ'] = 0
    selected_places['line_median'] = 0

    reversed_replace = (
        dict(zip(config['replace'].values(), config['replace'].keys()))
        )
    for i, r in selected_places.iterrows():
        s = r.place
        if s in reversed_replace:
            s = reversed_replace[s]
        idx = np.where(reader.detect_item(s))[0]
        selected_places.at[i, 'img'] = idx
        L = len(idx)
        selected_places.at[i, 'word_occ'] = L
        if (L == 0):
            selected_places.at[i, 'line_median'] = 0
        else:
            selected_places.at[i, 'line_median'] = np.median(idx)
    selected_places = selected_places[selected_places.word_occ >= 3]

    analyzer = Analyzer(CITIES)
    analyzer.resolve(config["resolve"])
    cities, ignored = analyzer.query(selected_places)
    print("***Ignored:", ignored)
    cities.sort_values("lng_srt").to_csv(OUTPUT, index=None)


if __name__ == "__main__":
    main()
