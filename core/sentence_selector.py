import re


class SentenceSelector:


    def __init__(self, max_sentences=5):
        self.max_sentences = max_sentences


    def split_sentences(self, text):

        return [
            s.strip()
            for s in re.split(
                r'[.!?]\s+',
                text
            )
            if len(s.strip()) > 20
        ]


    def select(self, context):

        sentences = []

        for item in context:

            text = item.get(
                "text",
                ""
            )

            for s in self.split_sentences(text):

                sentences.append(
                    {
                        "text": s,
                        "source": item.get(
                            "source",
                            ""
                        ),
                        "score": item.get(
                            "score",
                            0
                        )
                    }
                )


        sentences.sort(
            key=lambda x: x["score"],
            reverse=True
        )


        return sentences[:self.max_sentences]
