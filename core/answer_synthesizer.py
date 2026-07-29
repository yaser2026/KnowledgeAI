import re


class AnswerSynthesizer:


    def __init__(self, max_sentences=3):

        self.max_sentences = max_sentences



    def normalize(self, text):

        text = text.strip()

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text



    def synthesize(self, items):

        sentences = []

        seen = set()


        for item in items:

            text = item.get(
                "text",
                ""
            )

            if not text:
                continue


            text = self.normalize(
                text
            )


            parts = re.split(
                r'(?<=[.!?])\s+',
                text
            )


            for sentence in parts:

                sentence = sentence.strip()


                if len(sentence) < 30:
                    continue


                key = sentence.lower()


                if key not in seen:

                    seen.add(key)

                    sentences.append(
                        sentence
                    )


                if len(sentences) >= self.max_sentences:
                    break


            if len(sentences) >= self.max_sentences:
                break


        return sentences
