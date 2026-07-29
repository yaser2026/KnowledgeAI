import re


class QueryAnalyzer:

    def __init__(self):
        self.intent_keywords = {
            "definition": [
                "what is",
                "define",
                "چیست",
                "تعریف"
            ],

            "comparison": [
                "difference",
                "compare",
                "مقایسه",
                "تفاوت"
            ],

            "tutorial": [
                "how to",
                "how can",
                "چگونه",
                "آموزش"
            ],

            "error": [
                "error",
                "bug",
                "exception",
                "خطا",
                "مشکل"
            ],

            "code": [
                "code",
                "python",
                "java",
                "program",
                "کد",
                "برنامه نویسی"
            ]
        }


    def detect_language(self, text):
        if re.search(r"[\u0600-\u06FF]", text):
            return "fa"

        return "en"


    def normalize(self, text):
        text = text.lower().strip()

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text


    def detect_intent(self, text):

        text = self.normalize(text)

        scores = {}

        for intent, keywords in self.intent_keywords.items():

            score = 0

            for word in keywords:

                if word in text:
                    score += 1

            scores[intent] = score


        best = max(
            scores,
            key=scores.get
        )

        if scores[best] == 0:
            return "general"

        return best


    def extract_keywords(self, text):

        text = self.normalize(text)

        words = re.findall(
            r"\w+",
            text
        )

        keywords = []

        for word in words:

            if len(word) >= 3:
                keywords.append(word)


        return list(
            dict.fromkeys(keywords)
        )


    def analyze(self, question):

        return {
            "original": question,
            "normalized": self.normalize(question),
            "language": self.detect_language(question),
            "intent": self.detect_intent(question),
            "keywords": self.extract_keywords(question)
        }
