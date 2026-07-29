class KeywordRanker:


    def __init__(self):

        self.stop_words = {
            "such",
            "used",
            "using",
            "also",
            "many",
            "human",
            "system",
            "systems",
            "based",
            "make",
            "made",
            "like"
        }


        self.bad_names = {
            "russell",
            "norvig",
            "john",
            "peter",
            "alan",
            "michael"
        }



    def rank(self, keywords, limit=10):

        result = []


        for word in keywords:

            word = word.lower().strip()


            if word in self.stop_words:
                continue


            if word in self.bad_names:
                continue


            if word not in result:

                result.append(word)


            if len(result) >= limit:
                break


        return result



if __name__ == "__main__":

    r = KeywordRanker()


    print(
        r.rank(
            [
                "intelligence",
                "russell",
                "learning",
                "used",
                "machine",
                "norvig"
            ]
        )
    )
