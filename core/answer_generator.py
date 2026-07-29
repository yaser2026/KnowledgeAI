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


        for item in context:

            text = item.get(
                "text",
                ""
            )


            if text:

                answer.append(
                    "- " + text.strip()
                )


        return "\n".join(
            answer
        )
