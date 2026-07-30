from core.source_authority import SourceAuthority


class EvidenceRanker:


    def __init__(self):

        self.authority = SourceAuthority()



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


        authority = self.authority.get_score(
            item.get(
                "url",
                ""
            )
        )


        support_score = min(
            support / 5,
            1
        )


        score = (

            confidence * 0.35

            +

            support_score * 0.20

            +

            quality * 0.20

            +

            authority * 0.25

        )


        return round(
            min(score,1.0),
            2
        )



    def rank(self, evidence):


        for item in evidence:

            item["source_authority"] = self.authority.get_score(
                item.get(
                    "url",
                    ""
                )
            )


            item["evidence_score"] = self.score(
                item
            )


        return sorted(
            evidence,
            key=lambda x: x["evidence_score"],
            reverse=True
        )
