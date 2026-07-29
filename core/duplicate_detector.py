from core.text_similarity import TextSimilarity


class DuplicateDetector:

    def __init__(self, threshold=0.80):

        self.similarity = TextSimilarity()

        self.threshold = threshold


    def is_duplicate(
        self,
        text,
        existing_texts
    ):

        for existing in existing_texts:

            score = self.similarity.similarity(
                text,
                existing
            )

            if score >= self.threshold:

                return True, score

        return False, 0.0


if __name__ == "__main__":

    detector = DuplicateDetector()

    docs = [
        "Artificial intelligence is changing the world.",
        "Quantum computing is the future."
    ]

    print(
        detector.is_duplicate(
            "Artificial intelligence changes the world.",
            docs
        )
    )
