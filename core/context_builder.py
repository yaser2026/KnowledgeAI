from core.duplicate_filter import DuplicateFilter


class ContextBuilder:

    def __init__(
        self,
        max_chunks=5
    ):
        self.max_chunks = max_chunks
        self.duplicate_filter = DuplicateFilter()


    def build(
        self,
        items
    ):

        chunks = []

        for item in items:

            text = item.get(
                "content",
                ""
            )

            if not text:
                text = item.get(
                    "text",
                    ""
                )

            if not text:
                continue


            chunks.append(
                {
                    "text": text.strip(),
                    "source": item.get(
                        "title",
                        item.get(
                            "source",
                            "Unknown"
                        )
                    ),
                    "url": item.get(
                        "url",
                        ""
                    ),
                    "score": item.get(
                        "final_score",
                        item.get(
                            "score",
                            0
                        )
                    )
                }
            )


        chunks = self.duplicate_filter.filter(
            chunks
        )


        chunks = chunks[:self.max_chunks]


        chars = sum(
            len(
                c["text"]
            )
            for c in chunks
        )


        return {
            "context": chunks,
            "count": len(chunks),
            "chars": chars
        }
