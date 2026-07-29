import re


class TextSimilarity:

    def __init__(self):
        pass


    def normalize(self, text):

        if not text:
            return ""

        text = text.lower()

        text = re.sub(r"[^a-z0-9\s]", " ", text)

        text = re.sub(r"\s+", " ", text).strip()

        return text


    def tokenize(self, text):

        text = self.normalize(text)

        return set(text.split())


    def jaccard(self, text1, text2):

        a = self.tokenize(text1)
        b = self.tokenize(text2)

        if not a or not b:
            return 0.0

        return len(a & b) / len(a | b)


    def similarity(self, text1, text2):

        return round(
            self.jaccard(text1, text2),
            3
        )


if __name__ == "__main__":

    sim = TextSimilarity()

    print(
        sim.similarity(
            "Artificial intelligence is changing the world.",
            "Artificial intelligence changes the world."
        )
    )
