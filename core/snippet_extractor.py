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

        bad = [
            "please note",
            "welcome",
            "join the",
            "mailing list",
            "contact",
            "faq",
            "atom feed",
            "site news",
            "reporting issues"
        ]

        s = sentence.lower()

        return any(
            x in s
            for x in bad
        )


    def score_sentence(self, sentence, query):

        text = sentence.lower()
        q = query.lower()

        score = 0


        keywords = re.findall(
            r"[a-z0-9_]+",
            q
        )


        for word in keywords:

            if len(word) > 2 and word in text:
                score += 2


        concepts = [
            "is the",
            "is a",
            "core",
            "component",
            "manages",
            "controls",
            "provides",
            "system",
            "hardware",
            "software",
            "process",
            "memory",
            "cpu",
            "resource"
        ]


        for item in concepts:

            if item in text:
                score += 1


        if "what is" in q or "define" in q:

            if any(
                x in text
                for x in [
                    "is the",
                    "is a",
                    "core component",
                    "central part"
                ]
            ):
                score += 5


        if "documentation" in text:

            score -= 2


        return score



    def extract(self, text, query):

        sentences = self.split_sentences(
            text
        )

        scored = []


        for sentence in sentences:

            if self.is_noise(sentence):
                continue


            score = self.score_sentence(
                sentence,
                query
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
            s
            for _, s in scored[:self.max_sentences]
        ]
