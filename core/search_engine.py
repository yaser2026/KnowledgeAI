from core.providers.duckduckgo import DuckDuckGoProvider


class SearchEngine:


    def __init__(self):

        self.providers = {

            "duckduckgo": DuckDuckGoProvider()

        }



    def enhance_query(self, query):

        q = query.lower()


        keywords = [

            "linux",
            "kernel",
            "python",
            "database",
            "computer science",
            "ai"

        ]


        for k in keywords:

            if k in q:

                return (
                    query
                    +
                    " documentation official reference"
                )


        return query



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



        enhanced_query = self.enhance_query(
            query
        )


        results = engine.search(
            enhanced_query,
            limit
        )


        return results



if __name__ == "__main__":


    search = SearchEngine()


    results = search.search(
        "What is Linux kernel?",
        5
    )


    for item in results:

        print(item)
