import re


class SnippetExtractor:


    def __init__(self, max_sentences=5):

        self.max_sentences = max_sentences


    def split_sentences(self, text):

        if not text:
            return []

        return [
            s.strip()
            for s in re.split(
                r'(?<=[.!?])\s+',
                text
            )
            if len(s.strip()) > 30
        ]


    def extract(
        self,
        text,
        query
    ):

        sentences = self.split_sentences(text)

        if not sentences:
            return []


        keywords = {
            w.lower()
            for w in re.findall(
                r"[A-Za-z0-9_]+",
                query
            )
            if len(w) > 2
        }


        scored = []


        for sentence in sentences:

            lower = sentence.lower()

            score = sum(
                1
                for k in keywords
                if k in lower
            )

            if score:

                scored.append(
                    (
                        score,
                        sentence
                    )
                )


        scored.sort(
            reverse=True
        )


        return [
            s
            for _, s in scored[
                :self.max_sentences
            ]
        ]
