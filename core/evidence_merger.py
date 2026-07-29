import re


class EvidenceMerger:

    def __init__(self):
        pass


    def normalize(self, text):

        text = str(text).lower()

        text = re.sub(
            r'\s+',
            ' ',
            text
        )

        return text.strip()



    def get_text(self, item):

        return item.get(
            "text",
            item.get(
                "content",
                ""
            )
        )



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

            text = self.get_text(item)

            if not text:
                continue


            duplicate = False


            for old in merged:

                old_text = self.get_text(old)


                if self.similarity(
                    text,
                    old_text
                ) > 0.6:

                    old["support_count"] = old.get(
                        "support_count",
                        1
                    ) + 1

                    old["confidence"] = round(
                        min(
                            0.5 + old["support_count"] * 0.15,
                            1.0
                        ),
                        2
                    )

                    duplicate = True
                    break



            if not duplicate:

                item["support_count"] = 1

                item["confidence"] = round(
                    0.5 + item.get(
                        "content_quality",
                        0
                    ) * 0.5,
                    2
                )

                merged.append(
                    item
                )


        return merged
