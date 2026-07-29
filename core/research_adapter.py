from urllib.parse import urlparse


class ResearchAdapter:

    def __init__(self):
        pass


    def convert(self, urls):

        results = []

        total = len(urls)

        for index, url in enumerate(urls):

            results.append(
                {
                    "title": self.extract_title(url),
                    "url": url,
                    "content": "",
                    "search_score": round(
                        1 - (index / max(total, 1)),
                        2
                    ),
                    "research_score": 0.5,
                    "keyword_match": 0.5,
                    "content_quality": 0.5
                }
            )

        return results


    def extract_title(self, url):

        domain = urlparse(url).netloc

        return domain.replace(
            "www.",
            ""
        )
