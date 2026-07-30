class MultiSourceFusion:

    def __init__(self):
        pass


    def normalize_source(self, source):
        if not source:
            return ""

        source = source.lower()

        replacements = [
            "https://",
            "http://",
            "www."
        ]

        for r in replacements:
            source = source.replace(r, "")

        source = source.split("/")[0]

        return source.strip()


    def fuse(self, items):

        if not items:
            return []

        results = []
        seen = set()

        for item in items:

            title = item.get(
                "title",
                ""
            )

            url = item.get(
                "url",
                ""
            )

            source = self.normalize_source(
                url
            )

            if not source:
                source = self.normalize_source(
                    title
                )


            if source in seen:
                continue


            seen.add(source)

            results.append(item)


        return results
