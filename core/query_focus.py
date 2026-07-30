import re


class QueryFocus:


    def __init__(self):
        pass


    def filter(self, items, query):

        if not items:
            return []


        keywords = [
            x.lower()
            for x in re.findall(
                r"[A-Za-z0-9_]+",
                query
            )
            if len(x) > 2
        ]


        scored = []


        for item in items:

            text = item.get(
                "text",
                item.get(
                    "content",
                    ""
                )
            ).lower()


            score = sum(
                1
                for k in keywords
                if k in text
            )


            item["query_focus_score"] = score


            if score > 0:
                scored.append(item)


        return sorted(
            scored,
            key=lambda x: x["query_focus_score"],
            reverse=True
        )
