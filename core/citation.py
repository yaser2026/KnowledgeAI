class CitationManager:

    def __init__(self):
        pass


    def create_citation(self, source):

        return {
            "title": source.get(
                "title",
                source.get(
                    "source",
                    "Unknown Source"
                )
            ),

            "url": source.get(
                "url",
                ""
            ),

            "score": source.get(
                "evidence_score",
                source.get(
                    "final_score",
                    source.get(
                        "score",
                        0
                    )
                )
            )
        }


    def format(self, sources):

        citations = []

        for index, source in enumerate(
            sources,
            start=1
        ):

            item = self.create_citation(
                source
            )


            text = (
                f"[{index}] "
                f"{item['title']}"
            )


            if item["url"]:
                text += (
                    f" | {item['url']}"
                )


            text += (
                f" | Score: {item['score']}"
            )


            citations.append(text)


        return "\n".join(citations)
