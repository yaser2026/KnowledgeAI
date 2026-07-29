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



    def calculate_confidence(self, item, support_count):

        score = 0.5


        if support_count > 1:
            score += 0.1 * min(
                support_count,
                5
            )


        if item.get("source"):
            score += 0.1


        if item.get("title"):
            score += 0.05


        return min(
            round(score, 2),
            1.0
        )



    def merge(self, items):

        merged = []


        for item in items:

            text = item.get(
                "text",
                ""
            )


            if not text:
                continue


            found = False


            for old in merged:

                similarity = self.similarity(
                    text,
                    old["text"]
                )


                if similarity > 0.6:

                    old["support_count"] += 1

                    old["confidence"] = self.calculate_confidence(
                        old,
                        old["support_count"]
                    )

                    found = True
                    break



            if not found:

                new_item = dict(item)

                new_item["support_count"] = 1

                new_item["confidence"] = self.calculate_confidence(
                    new_item,
                    1
                )

                merged.append(
                    new_item
                )


        return merged
