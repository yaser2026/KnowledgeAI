import re


class DuplicateFilter:


    def normalize(self, text):

        text = text.lower()

        text = re.sub(
            r'[^a-z0-9\s]',
            '',
            text
        )

        return text.strip()



    def filter(self, items):

        result = []
        seen = set()

        for item in items:

            text = item.get(
                "text",
                ""
            )

            key = self.normalize(
                text
            )

            if key and key not in seen:

                seen.add(key)
                result.append(item)


        return result
