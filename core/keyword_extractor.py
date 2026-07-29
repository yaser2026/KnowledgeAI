import re
from collections import Counter


class KeywordExtractor:


    def extract(
        self,
        text,
        limit=10
    ):

        words = re.findall(
            r'\b[a-zA-Z]{4,}\b',
            text.lower()
        )


        stopwords = {
            "this",
            "that",
            "with",
            "from",
            "have",
            "been",
            "which",
            "about",
            "into",
            "using",
            "their"
        }


        words = [
            w for w in words
            if w not in stopwords
        ]


        counts = Counter(words)


        return [
            word
            for word, count
            in counts.most_common(limit)
        ]



if __name__ == "__main__":

    extractor = KeywordExtractor()


    text = """
    Artificial intelligence and machine learning
    are important fields of computer science.
    Deep learning uses neural networks.
    """


    print(
        extractor.extract(text)
    )
