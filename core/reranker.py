class ReRanker:

    def __init__(self):
        self.weights = {
            "search_score": 0.40,
            "research_score": 0.25,
            "keyword_match": 0.20,
            "content_quality": 0.15
        }


    def calculate_score(self, result):

        score = 0

        score += (
            result.get("search_score", 0)
            *
            self.weights["search_score"]
        )

        score += (
            result.get("research_score", 0)
            *
            self.weights["research_score"]
        )

        score += (
            result.get("keyword_match", 0)
            *
            self.weights["keyword_match"]
        )

        score += (
            result.get("content_quality", 0)
            *
            self.weights["content_quality"]
        )

        return round(score, 4)


    def rerank(self, results):

        ranked = []

        for item in results:

            item["final_score"] = self.calculate_score(item)

            ranked.append(item)


        ranked.sort(
            key=lambda x: x["final_score"],
            reverse=True
        )

        return ranked
