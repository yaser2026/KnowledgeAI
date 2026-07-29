class CitationDeduplicator:


    def __init__(self):
        pass


    def deduplicate(self, citations):

        if not citations:
            return []


        if isinstance(citations, str):
            citations = citations.split("\n")


        result = []
        seen = set()


        for item in citations:

            key = item.strip()

            if not key:
                continue


            if key not in seen:

                seen.add(key)

                result.append(
                    key
                )


        return result
