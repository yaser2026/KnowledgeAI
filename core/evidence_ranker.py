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

        source_score = item.get(
            "source_score",
            0.5
        )


        support_score = min(
            support / 5,
            1
        )


        score = (
            confidence * 0.35
            +
            support_score * 0.25
            +
            quality * 0.25
            +
            source_score * 0.15
        )


        return round(
            min(score, 1.0),
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
