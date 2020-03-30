"""Analyzer module: utilities to manipulate list of cities."""

import pandas as pd


def normalize(x):
    """Normalize longitude."""
    if x < -0.2:
        x += 360
    return x


class Analyzer():
    """Class to analyze and manipulate list of cities."""

    def __init__(self, file):
        """Init class."""
        self.df = pd.read_csv(file)
        self.normalize_lng("lng_srt")

    def query(self, places):
        """Query a list or dataframe of places in the internal list."""
        if (type(places)) is str:
            places = [places]

        if type(places) is list:
            places = pd.DataFrame(pd.Series(places), columns=["place"])

        merged = places.merge(
            self.df,
            how="left",
            left_on="place",
            right_on="city")

        # Remove empty rows
        indices = merged[merged.city.isnull()].index
        ignored = merged.loc[indices, "place"]
        return merged.drop(indices), ignored

    def resolve(self, resolve_list):
        """Resolve duplicates entry based on given list."""
        for r in resolve_list:
            indices = self.df[
                (self.df.city == r[0]) & (self.df[r[1]] != r[2])
                ].index
            print("***", indices)
            self.df.drop(indices, inplace=True)

    def distill(self):
        """Remove rows with empty fields."""
        indices = self.df[self.city == ""].index
        self.df.drop(indices, inplace=True)

    def normalize_lng(self, newcol):
        """Normalize longitude to range [0,360)."""
        self.df[newcol] = self.df.lng.apply(normalize)
