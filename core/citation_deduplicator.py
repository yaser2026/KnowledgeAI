class CitationDeduplicator:


    def __init__(self):
        pass


    def extract_source(self, text):

        text = text.strip()

        if "|" in text:

            parts = text.split("|")

            return parts[0].strip()


        return text



    def deduplicate(self, citations):

        if not citations:
            return []


        result=[]

        seen=set()


        for item in citations:


            if not item:
                continue


            source = self.extract_source(
                item
            )


            key = source.lower()


            if key not in seen:

                seen.add(key)

                result.append(
                    item
                )


        return result
