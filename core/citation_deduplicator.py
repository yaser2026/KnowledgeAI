import re


class CitationDeduplicator:


    def __init__(self):
        pass


    def extract_source(self, text):

        text = text.strip()

        text = re.sub(
            r"^\[\d+\]\s*",
            "",
            text
        )

        source = text.split(
            "|"
        )[0].strip()

        return source



    def deduplicate(self, citations):

        if not citations:
            return []


        if isinstance(citations, str):

            citations = citations.split(
                "\n"
            )


        result = []
        seen = set()


        for item in citations:

            if not item:
                continue


            source = self.extract_source(
                item
            )


            if source not in seen:

                seen.add(source)

                result.append(
                    item
                )


        return result
