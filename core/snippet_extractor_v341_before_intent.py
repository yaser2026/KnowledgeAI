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


    def is_noise(self, sentence):

        bad_patterns = [
            "please note",
            "welcome",
            "join the",
            "community",
            "mailing list",
            "contact",
            "faq",
            "atom feed",
            "site news"
        ]

        lower = sentence.lower()

        for pattern in bad_patterns:
            if pattern in lower:
                return True

        return False



    def score_sentence(
        self,
        sentence,
        keywords
    ):

        lower = sentence.lower()

        score = 0


        for word in keywords:

            if word in lower:
                score += 1


        important = [
            "kernel",
            "linux",
            "operating system",
            "hardware",
            "software",
            "process",
            "memory",
            "cpu",
            "scheduler",
            "resource"
        ]


        for word in important:

            if word in lower:
                score += 0.5


        return score



    def extract(
        self,
        text,
        query
    ):


        sentences = self.split_sentences(
            text
        )


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


            if self.is_noise(sentence):

                continue


            score = self.score_sentence(
                sentence,
                keywords
            )


            if score > 0:

                scored.append(
                    (
                        score,
                        sentence
                    )
                )


        scored.sort(
            key=lambda x: x[0],
            reverse=True
        )


        return [
            sentence
            for score, sentence in scored[
                :self.max_sentences
            ]
        ]
