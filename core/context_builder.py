import re


class ContextBuilder:

    def __init__(self, max_chunks=5):
        self.max_chunks = max_chunks


    def clean_text(self, text):

        text = text.strip()

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text


    def remove_duplicates(self, chunks):

        seen = set()
        unique = []

        for chunk in chunks:

            key = chunk[:100].lower()

            if key not in seen:
                seen.add(key)
                unique.append(chunk)

        return unique


    def build(self, results):

        chunks = []

        for item in results:

            content = item.get(
                "content",
                ""
            )

            if content:

                chunks.append(
                    self.clean_text(content)
                )


        chunks = self.remove_duplicates(chunks)


        return {
            "context": chunks[:self.max_chunks],
            "count": len(chunks[:self.max_chunks])
        }
