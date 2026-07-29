class ConfidenceEngine:

    def __init__(self):
        pass


    def calculate(self, evidence):

        if not evidence:
            return 0.0


        total = 0

        for item in evidence:

            total += item.get(
                "confidence",
                0
            )


        score = total / len(evidence)


        return round(
            min(score, 1.0),
            2
        )
