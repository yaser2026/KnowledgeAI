class KeywordFilter:


    def __init__(self):

        self.bad_words = {

            "retrieved",
            "archived",
            "original",

            "january",
            "february",
            "march",
            "april",
            "may",
            "june",
            "july",
            "august",
            "september",
            "october",
            "november",
            "december",

            "using",
            "also",
            "more",
            "many",

            "they",
            "their",
            "them",
            "this",
            "that",
            "these",
            "those",

            "such",
            "used"
        }



    def filter(self, keywords):

        return [
            k
            for k in keywords
            if k.lower()
            not in self.bad_words
        ]
