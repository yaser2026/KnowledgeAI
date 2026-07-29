class Classifier:


    def __init__(self):

        self.categories = {

            "AI": [
                "artificial intelligence",
                "machine learning",
                "deep learning",
                "neural network",
                "ai"
            ],


            "Programming": [
                "python",
                "java",
                "javascript",
                "programming",
                "algorithm",
                "code"
            ],


            "Linux": [
                "linux",
                "kernel",
                "ubuntu",
                "bash",
                "unix"
            ],


            "Database": [
                "database",
                "sql",
                "sqlite",
                "mysql"
            ],


            "Security": [
                "security",
                "hacking",
                "cryptography",
                "malware"
            ]

        }



    def classify(self, text):

        if not text:
            return "Unknown"


        text = text.lower()


        scores = {}


        for category, keywords in self.categories.items():

            score = 0

            for keyword in keywords:

                if keyword in text:
                    score += 1


            scores[category] = score



        best = max(
            scores,
            key=scores.get
        )


        if scores[best] == 0:
            return "Unknown"


        return best



if __name__ == "__main__":


    classifier = Classifier()


    text = """
    Linux kernel is written in C language.
    Python programming is also popular.
    """


    print(
        classifier.classify(text)
    )
