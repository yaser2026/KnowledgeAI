import re


class Summarizer:


    def split_sentences(self, text):

        sentences = re.split(
            r'(?<=[.!?])\s+',
            text
        )

        return [
            s.strip()
            for s in sentences
            if len(s.strip()) > 30
        ]



    def summarize(
        self,
        text,
        max_sentences=5
    ):

        if not text:
            return ""


        sentences = self.split_sentences(
            text
        )


        if len(sentences) <= max_sentences:

            return " ".join(sentences)


        # انتخاب جملات ابتدایی به عنوان خلاصه اولیه
        summary = sentences[:max_sentences]


        return " ".join(summary)



if __name__ == "__main__":


    summarizer = Summarizer()


    text = """
    Artificial intelligence is a branch of computer science.
    It focuses on creating intelligent systems.
    Machine learning is one of the important areas of AI.
    Deep learning uses neural networks.
    AI is used in many industries today.
    """


    print(
        summarizer.summarize(text)
    )
