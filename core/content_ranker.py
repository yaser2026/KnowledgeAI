class ContentRanker:

    def __init__(self):
        pass


    def score(
        self,
        title,
        content
    ):

        score = 0

        if title:
            score += 20

        length = len(content)

        if length > 1000:
            score += 40
        elif length > 500:
            score += 30
        elif length > 200:
            score += 20
        else:
            score += 10

        words = len(content.split())

        score += min(40, words // 25)

        return min(score, 100)


if __name__ == "__main__":

    ranker = ContentRanker()

    print(
        ranker.score(
            "Artificial Intelligence",
            "Artificial intelligence " * 300
        )
    )
