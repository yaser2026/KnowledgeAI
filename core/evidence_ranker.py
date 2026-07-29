class EvidenceRanker:

    def __init__(self):
        pass


    def score(self, item):

        confidence = item.get(
            "confidence",
            0
        )

        support = item.get(
            "support_count",
            1
        )

        quality = item.get(
            "content_quality",
            0
        )


        score = (
            confidence * 0.5
            +
            min(support / 5, 1) * 0.3
            +
            quality * 0.2
        )


        return round(
            score,
            2
        )


    def rank(self, evidence):

        for item in evidence:

            item["evidence_score"] = self.score(
                item
            )


        return sorted(
            evidence,
            key=lambda x: x["evidence_score"],
            reverse=True
        )
