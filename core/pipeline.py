from core.downloader import Downloader
from core.extractor import Extractor
from core.cleaner import Cleaner
from core.classifier import Classifier
from core.database import Database


class Pipeline:


    def __init__(self):

        self.downloader = Downloader()
        self.extractor = Extractor()
        self.cleaner = Cleaner()
        self.classifier = Classifier()
        self.database = Database()



    def process(self, title, url):

        print("[1] Downloading...")

        html = self.downloader.download(url)


        if not html:
            print("Download failed")
            return None



        print("[2] Extracting...")

        text = self.extractor.extract(html)


        if not text:
            print("Extraction failed")
            return None



        print("[3] Cleaning...")

        clean_text = self.cleaner.clean(text)



        print("[4] Classifying...")

        category = self.classifier.classify(
            clean_text
        )



        print("[5] Saving...")

        article_id = self.database.add_article(
            title,
            url,
            clean_text,
            "",
            category
        )


        print(
            "Saved article:",
            article_id
        )


        return article_id



if __name__ == "__main__":


    pipeline = Pipeline()


    pipeline.process(
        "Example Article",
        "https://example.com"
    )
