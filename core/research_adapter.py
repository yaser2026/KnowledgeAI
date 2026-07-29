from urllib.parse import urlparse

from core.downloader import Downloader
from core.extractor import Extractor
from core.cleaner import Cleaner


class ResearchAdapter:

    def __init__(self):

        self.downloader = Downloader()
        self.extractor = Extractor()
        self.cleaner = Cleaner()


    def convert(self, urls):

        results = []

        total = len(urls)

        for index, url in enumerate(urls):

            content = self.extract_content(url)

            results.append(
                {
                    "title": self.extract_title(url),
                    "url": url,
                    "content": content,

                    "search_score": round(
                        1 - (index / max(total, 1)),
                        2
                    ),

                    "research_score": self.research_score(
                        content
                    ),

                    "keyword_match": 0.5,

                    "content_quality": self.content_quality(
                        content
                    )
                }
            )

        return results


    def extract_content(self, url):

        try:

            html = self.downloader.download(
                url
            )

            if not html:
                return ""

            text = self.extractor.extract(
                html
            )

            if not text:
                return ""

            return self.cleaner.clean(
                text
            )

        except Exception:

            return ""


    def extract_title(self, url):

        return urlparse(url).netloc.replace(
            "www.",
            ""
        )


    def content_quality(self, text):

        length = len(text)

        if length > 3000:
            return 1.0

        if length > 1000:
            return 0.8

        if length > 300:
            return 0.6

        return 0.2


    def research_score(self, text):

        if len(text) > 1000:
            return 0.8

        if len(text) > 300:
            return 0.6

        return 0.3
