class ConfidenceEngine:

    def __init__(self):
        pass


    def calculate(self, evidence):

        if not evidence:
            return 0.0


        confidence_sum = 0
        evidence_sum = 0


        for item in evidence:

            confidence_sum += item.get(
                "confidence",
                0
            )

            evidence_sum += item.get(
                "evidence_score",
                0
            )


        avg_confidence = confidence_sum / len(evidence)

        avg_evidence = evidence_sum / len(evidence)


        count_bonus = min(
            len(evidence) / 5,
            1
        )


        final = (
            avg_confidence * 0.45
            +
            avg_evidence * 0.35
            +
            count_bonus * 0.20
        )


        return round(
            min(final,1.0),
            2
        )
