import re


class SentenceSelector:

    def __init__(self, max_sentences=5):
        self.max_sentences = max_sentences

    def clean_sentence(self, text):
        text = text.strip()

        text = re.sub(
            r'^\-\s*',
            '',
            text
        )

        text = re.sub(
            r'\s+',
            ' ',
            text
        )

        return text.strip()

    def split_sentences(self, text):
        parts = re.split(
            r'(?<=[.!?])\s+',
            text
        )

        return [
            p.strip()
            for p in parts
            if len(p.strip()) > 30
        ]

    def select(self, data):

        results = []

        seen_sentences = set()
        seen_sources = set()

        for item in data:

            text = item.get("text", "")

            source = (
                item.get("url")
                or item.get("title")
                or item.get("source")
                or ""
            )

            sentences = self.split_sentences(text)

            for sentence in sentences:

                sentence = self.clean_sentence(sentence)

                key = sentence.lower()

                if key in seen_sentences:
                    continue

                if source in seen_sources:
                    continue

                seen_sentences.add(key)
                seen_sources.add(source)

                results.append({
                    "text": sentence,
                    "title": item.get(
                        "title",
                        item.get("source", "")
                    ),
                    "url": item.get("url", ""),
                    "score": item.get(
                        "evidence_score",
                        item.get(
                            "score",
                            0
                        )
                    )
                })

                if len(results) >= self.max_sentences:
                    return results

        return results
