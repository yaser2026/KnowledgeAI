import re


class SentenceSelector:

    def __init__(
        self,
        max_sentences=5
    ):
        self.max_sentences = max_sentences


    def clean_sentence(self, text):

        text = text.strip()

        text = re.sub(
            r'^\-\s*',
            '',
            text
        )

        text = re.sub(
            r'\s+',
            ' ',
            text
        )

        return text.strip()



    def split_sentences(self, text):

        parts = re.split(
            r'(?<=[.!?])\s+',
            text
        )

        return [
            p.strip()
            for p in parts
            if len(p.strip()) > 30
        ]



    def select(self, data):

        results = []

        seen = set()


        for item in data:

            text = item.get(
                "text",
                ""
            )


            sentences = self.split_sentences(
                text
            )


            for sentence in sentences:

                sentence = self.clean_sentence(
                    sentence
                )


                key = sentence.lower()


                if key in seen:
                    continue


                seen.add(key)


                result = dict(item)


                # حفظ متن انتخاب شده
                result["text"] = sentence


                # حفظ امتیاز واقعی evidence
                result["score"] = item.get(
                    "evidence_score",
                    item.get(
                        "final_score",
                        item.get(
                            "score",
                            0
                        )
                    )
                )


                # حفظ عنوان و URL منبع
                result["title"] = item.get(
                    "title",
                    item.get(
                        "source",
                        "Unknown Source"
                    )
                )


                result["url"] = item.get(
                    "url",
                    ""
                )


                results.append(
                    result
                )


                if len(results) >= self.max_sentences:

                    return results


        return results
