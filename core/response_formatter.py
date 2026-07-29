class ResponseFormatter:


    def format(
        self,
        answer,
        citations=None
    ):

        if not answer:
            return {
                "answer": "",
                "citations": citations or []
            }


        text = answer.strip()


        if "Question:" in text:

            text = text.replace(
                "Question:",
                ""
            ).strip()


        if "Answer:" in text:

            text = text.split(
                "Answer:",
                1
            )[1].strip()


        if "Sources:" in text:

            text = text.split(
                "Sources:",
                1
            )[0].strip()


        return {
            "answer": text,
            "citations": citations or []
        }
