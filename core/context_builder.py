import re


class ContextBuilder:

    def __init__(self, max_chunks=5, max_chars=5000):
        self.max_chunks = max_chunks
        self.max_chars = max_chars


    def clean_text(self, text):

        text = text.strip()

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text


    def split_sentences(self, text):

        return re.split(
            r'(?<=[.!?])\s+',
            text
        )


    def remove_duplicates(self, items):

        seen = set()
        result = []

        for item in items:

            key = item["text"][:100].lower()

            if key not in seen:

                seen.add(key)
                result.append(item)

        return result


    def build(self, results):

        chunks = []

        for item in results:

            content = item.get(
                "content",
                ""
            )

            if not content:
                continue


            text = self.clean_text(
                content
            )


            sentences = self.split_sentences(
                text
            )


            for sentence in sentences:

                if len(sentence.strip()) < 40:
                    continue


                chunks.append(
                    {
                        "text": sentence.strip(),
                        "source": item.get(
                            "title",
                            "Unknown"
                        ),
                        "url": item.get(
                            "url",
                            ""
                        ),
                        "score": item.get(
                            "final_score",
                            0
                        )
                    }
                )


        chunks = self.remove_duplicates(
            chunks
        )


        selected = []

        size = 0


        for chunk in chunks:

            if len(selected) >= self.max_chunks:
                break


            length = len(
                chunk["text"]
            )


            if size + length > self.max_chars:
                break


            selected.append(
                chunk
            )

            size += length


        return {
            "context": selected,
            "count": len(selected),
            "chars": size
        }
