from core.providers.duckduckgo import DuckDuckGoProvider


class SearchEngine:


    def __init__(self):

        self.providers = {
            "duckduckgo":
            DuckDuckGoProvider()
        }



    def search(
        self,
        query,
        limit=5,
        provider="duckduckgo"
    ):

        engine = self.providers.get(
            provider
        )


        if not engine:

            return []


        return engine.search(
            query,
            limit
        )



if __name__ == "__main__":


    search = SearchEngine()


    results = search.search(
        "Artificial Intelligence",
        5
    )


    for item in results:

        print(item)
