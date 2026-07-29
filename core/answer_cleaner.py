import re


class AnswerCleaner:


    def clean(self, text):

        if not text:
            return ""


        text = re.sub(
            r'\[\d+\](?::\s*\d+)?',
            '',
            text
        )


        text = re.sub(
            r'\[[0-9,\s]+\]',
            '',
            text
        )


        lines = []

        blocked = [
            "Original author",
            "Stable release",
            "Written in",
            "License",
            "Website",
            "Repository"
        ]


        for line in text.split("\n"):

            skip = False

            for word in blocked:

                if word.lower() in line.lower():
                    skip = True
                    break


            if not skip:
                lines.append(line)


        result = "\n".join(lines)


        result = re.sub(
            r'\s+',
            ' ',
            result
        )


        return result.strip()
