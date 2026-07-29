from urllib.parse import quote


class SearchEngine:

    def __init__(self):
        self.engines = {
            "google": "https://www.google.com/search?q=",
            "bing": "https://www.bing.com/search?q="
        }


    def create_search_url(self, query, engine="google"):

        if engine not in self.engines:
            engine = "google"

        return self.engines[engine] + quote(query)


    def search_info(self, query):

        return {
            "query": query,
            "engine": "google",
            "url": self.create_search_url(query)
        }


if __name__ == "__main__":

    search = SearchEngine()

    result = search.search_info(
        "Artificial Intelligence"
    )

    print(result)
