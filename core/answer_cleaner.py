import re


class AnswerCleaner:


    def clean(self, text):

        if not text:
            return ""


        # Remove wikipedia references
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


        patterns = [
            r'Original author.*?(?=\.|$)',
            r'Stable release.*?(?=\.|$)',
            r'Written in.*?(?=\.|$)',
            r'License.*?(?=\.|$)',
            r'Website.*?(?=\.|$)',
            r'Repository.*?(?=\.|$)'
        ]


        for pattern in patterns:

            text = re.sub(
                pattern,
                '',
                text,
                flags=re.I
            )


        # Clean broken punctuation
        text = re.sub(
            r'\.{2,}',
            '.',
            text
        )


        text = re.sub(
            r'\s+\.',
            '.',
            text
        )


        text = re.sub(
            r'\s+',
            ' ',
            text
        )


        return text.strip()
