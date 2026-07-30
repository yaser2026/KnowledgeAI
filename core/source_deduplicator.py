class SourceDeduplicator:

    def __init__(self):
        pass


    def normalize(self, item):

        url = item.get(
            "url",
            ""
        )

        if url:

            url = (
                url.lower()
                .replace("https://", "")
                .replace("http://", "")
                .replace("www.", "")
            )

            return url.split("/")[0].strip()


        title = item.get(
            "title",
            ""
        )

        return title.lower().strip()



    def deduplicate(self, items):

        if not items:
            return []


        results = []

        seen = set()


        for item in items:

            source = self.normalize(
                item
            )


            if not source:
                continue


            if source in seen:
                continue


            seen.add(
                source
            )


            results.append(
                item
            )


        return results
