class CitationManager:

    def __init__(self):
        pass


    def create_citation(self, source):

        citation = {}

        citation["title"] = source.get(
            "title",
            "Unknown Source"
        )

        citation["book"] = source.get(
            "book",
            ""
        )

        citation["chapter"] = source.get(
            "chapter",
            ""
        )

        citation["page"] = source.get(
            "page",
            ""
        )

        return citation


    def format(self, sources):

        citations = []

        for index, source in enumerate(
            sources,
            start=1
        ):

            item = self.create_citation(source)

            text = f"[{index}] {item['title']}"

            if item["book"]:
                text += f" | Book: {item['book']}"

            if item["chapter"]:
                text += f" | Chapter: {item['chapter']}"

            if item["page"]:
                text += f" | Page: {item['page']}"

            citations.append(text)


        return "\n".join(citations)
