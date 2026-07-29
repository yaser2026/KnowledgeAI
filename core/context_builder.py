import re


class ContextBuilder:

    def __init__(self, max_chunks=5, max_chars=5000):
        self.max_chunks = max_chunks
        self.max_chars = max_chars


    def clean_text(self, text):

        text = text.strip()

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text


    def split_sentences(self, text):

        return re.split(
            r'(?<=[.!?])\s+',
            text
        )


    def remove_duplicates(self, items):

        seen = set()
        result = []

        for item in items:

            key = item[:100].lower()

            if key not in seen:

                seen.add(key)
                result.append(item)

        return result


    def build(self, results):

        all_text = []

        for item in results:

            content = item.get(
                "content",
                ""
            )

            if content:

                text = self.clean_text(
                    content
                )

                sentences = self.split_sentences(
                    text
                )

                all_text.extend(
                    sentences
                )


        all_text = self.remove_duplicates(
            all_text
        )


        context = []

        size = 0

        for sentence in all_text:

            if len(context) >= self.max_chunks:
                break


            if size + len(sentence) > self.max_chars:
                break


            context.append(sentence)
            size += len(sentence)


        return {
            "context": context,
            "count": len(context),
            "chars": size
        }
