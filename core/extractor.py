import trafilatura


class Extractor:

    def extract(self, html):

        if not html:
            return None

        text = trafilatura.extract(
            html,
            include_comments=False,
            include_tables=True
        )

        return text


if __name__ == "__main__":

    from downloader import Downloader


    downloader = Downloader()

    html = downloader.download(
        "https://example.com"
    )


    extractor = Extractor()

    text = extractor.extract(html)


    if text:
        print(text[:500])
    else:
        print("No text extracted")
