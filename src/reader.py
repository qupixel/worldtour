"""Reader module."""

import numpy as np
# from geotext import GeoText
import spacy


def detect(s, lines):
    """Detect a string in a list of strings."""
    pholder = np.zeros((len(lines),))
    for i, l in enumerate(lines):
        if s in l:
            pholder[i] += 1
    return pholder


class BookReader():
    """Class to access and manipulate texts."""

    def __init__(self, src, start_term=None, end_term=None):
        """Init."""
        self.nlp = spacy.load("en_core_web_sm")

        self._chapters = None

        with open(src, encoding='utf-8') as f:
            lines = f.readlines()

        if start_term is not None:
            start_line = np.where(detect(start_term, lines))[0][0]
        else:
            start_line = 0

        if end_term is not None:
            end_line = np.where(detect(end_term, lines))[0][0]
        else:
            end_line = len(lines)

        self._lines = lines[start_line:end_line]

    def detect_item(self, s):
        """Detect a string in the lines of this ebook."""
        return detect(s, self._lines)

    def _extract_chapter_limits(self):
        """Get chapter limits."""
        n = len(self._lines)
        chapter_lines = np.append(
            np.where(detect("Chapter ", self._lines))[0], [n]
            )
        return chapter_lines

    def _extract_chapter(self, chapter):
        """Get chapter using chapter limits."""
        chapter_lines = self._extract_chapter_limits()
        return self._lines[chapter_lines[chapter]:chapter_lines[chapter+1]]

    def _parse_chapters(self):
        """Get all chapters as a list of strings."""
        self._chapters = [self._extract_chapter(c) for c in range(0, 37)]

    def find_places(self, s, replace_dict={}, ignore_list=[]):
        """Find places in a string using spacy."""
        places = []
        doc = self.nlp(s)

        for ent in doc.ents:
            if ent.label_ == "GPE":
                if ent.text in ignore_list:
                    continue
                if ent.text in replace_dict:
                    places += [replace_dict[ent.text]]
                else:
                    places += [ent.text]

        return places
