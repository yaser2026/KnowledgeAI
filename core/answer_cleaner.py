import re


class AnswerCleaner:


    def clean(self, text):

        if not text:
            return ""


        # Remove references like [16]:4
        text = re.sub(
            r'\[\d+\](?::\s*\d+)?',
            '',
            text
        )


        # Remove metadata phrases but keep remaining sentence
        remove_patterns = [
            r'Original author\s+[^.]+\.?',
            r'License\s+[^.]+\.?',
            r'Stable release\s+[^.]+\.?',
            r'Written in\s+[^.]+\.?',
            r'Website\s+[^.]+\.?',
            r'Repository\s+[^.]+\.?'
        ]


        for pattern in remove_patterns:
            text = re.sub(
                pattern,
                '',
                text,
                flags=re.I
            )


        # Fix punctuation artifacts
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
