import re


class EvidenceMerger:

    def __init__(self):
        pass


    def normalize(self, text):

        text = text.lower()

        text = re.sub(
            r'\s+',
            ' ',
            text
        )

        return text.strip()


    def similarity(self, a, b):

        a_words = set(
            self.normalize(a).split()
        )

        b_words = set(
            self.normalize(b).split()
        )

        if not a_words or not b_words:
            return 0

        return len(
            a_words & b_words
        ) / len(
            a_words | b_words
        )


    def merge(self, items):

        merged = []

        for item in items:

            text = item.get(
                "text",
                ""
            )

            duplicate = False

            for old in merged:

                if self.similarity(
                    text,
                    old["text"]
                ) > 0.6:

                    duplicate = True

                    break


            if not duplicate:
                merged.append(item)


        return merged
