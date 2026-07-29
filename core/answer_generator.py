class AnswerGenerator:


    def __init__(self):
        pass


    def build_answer(
        self,
        question,
        context,
        citations=None
    ):

        answer = []

        answer.append(
            f"Question: {question}\n"
        )


        answer.append(
            "Answer:\n"
        )


        for item in context:

            text = item.get(
                "text",
                ""
            )

            if text:

                answer.append(
                    "- " + text
                )


        if citations:

            answer.append(
                "\nSources:\n"
            )

            answer.append(
                citations
            )


        return "\n".join(
            answer
        )
