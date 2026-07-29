from bs4 import BeautifulSoup
from urllib.parse import urlparse


class SearchParser:


    def extract_links(self, html, limit=5):

        if not html:
            return []


        soup = BeautifulSoup(
            html,
            "lxml"
        )


        links = []


        for a in soup.find_all("a"):

            href = a.get("href")


            if not href:
                continue


            if href.startswith("http"):

                domain = urlparse(href).netloc


                if domain not in [
                    "google.com",
                    "www.google.com"
                ]:

                    links.append(href)



            if len(links) >= limit:
                break


        return links



if __name__ == "__main__":

    parser = SearchParser()

    test_html = """
    <a href="https://example.com/page">
    Example
    </a>
    """

    print(
        parser.extract_links(test_html)
    )
