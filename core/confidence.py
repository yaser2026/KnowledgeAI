class ConfidenceEngine:


    def __init__(self):
        pass



    def calculate(self, evidence):


        if not evidence:
            return 0.0


        confidence_sum = 0.0
        evidence_sum = 0.0
        authority_sum = 0.0


        for item in evidence:

            confidence_sum += item.get(
                "confidence",
                0.0
            )

            evidence_sum += item.get(
                "evidence_score",
                0.0
            )

            authority_sum += item.get(
                "source_authority",
                0.30
            )


        count = len(evidence)

        avg_confidence = confidence_sum / count
        avg_evidence = evidence_sum / count
        avg_authority = authority_sum / count

        count_bonus = min(
            count / 5,
            1.0
        )


        final = (

            avg_confidence * 0.35

            +

            avg_evidence * 0.30

            +

            avg_authority * 0.20

            +

            count_bonus * 0.15

        )


        return round(
            min(final, 1.0),
            2
        )
