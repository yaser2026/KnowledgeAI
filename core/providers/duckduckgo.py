import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urlparse, parse_qs, unquote


class DuckDuckGoProvider:


    def __init__(self):

        self.url = (
            "https://html.duckduckgo.com/html/?q="
        )

        self.headers = {
            "User-Agent":
            "Mozilla/5.0"
        }



    def clean_url(self, url):

        if "uddg=" in url:

            parsed = urlparse(url)

            params = parse_qs(
                parsed.query
            )

            if "uddg" in params:

                return unquote(
                    params["uddg"][0]
                )


        if url.startswith("//"):

            return "https:" + url


        return url



    def search(self, query, limit=5):

        try:

            response = requests.get(
                self.url + quote(query),
                headers=self.headers,
                timeout=15
            )

            response.raise_for_status()


            soup = BeautifulSoup(
                response.text,
                "lxml"
            )


            results = []


            for link in soup.select(
                ".result__a"
            ):

                href = link.get("href")


                if href:

                    href = self.clean_url(
                        href
                    )

                    results.append(
                        href
                    )


                if len(results) >= limit:
                    break


            return results


        except Exception as e:

            print(
                "DuckDuckGo error:",
                e
            )

            return []



if __name__ == "__main__":

    engine = DuckDuckGoProvider()


    results = engine.search(
        "Artificial Intelligence",
        5
    )


    for r in results:
        print(r)
