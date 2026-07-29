from core.search_engine import SearchEngine
from core.downloader import Downloader
from core.extractor import Extractor
from core.cleaner import Cleaner
from core.classifier import Classifier
from core.database import Database
from core.article_info import ArticleInfo


class Pipeline:


    def __init__(self):

        self.search = SearchEngine()

        self.downloader = Downloader()

        self.extractor = Extractor()

        self.cleaner = Cleaner()

        self.classifier = Classifier()

        self.database = Database()

        self.info = ArticleInfo()



    def process_article(self, url):

        print("\nURL:")
        print(url)


        print("[1] Downloading...")


        html = self.downloader.download(
            url
        )


        if not html:

            print("Download failed")

            return None



        print("[2] Extracting metadata...")


        metadata = self.info.extract(
            html
        )


        title = metadata.get(
            "title",
            "Unknown Article"
        )


        print(
            "Title:",
            title
        )



        print("[3] Extracting text...")


        text = self.extractor.extract(
            html
        )


        if not text:

            print(
                "Extraction failed"
            )

            return None



        print("[4] Cleaning...")


        clean_text = self.cleaner.clean(
            text
        )



        print("[5] Classifying...")


        category = self.classifier.classify(
            clean_text
        )



        print("[6] Saving...")


        article_id = self.database.add_article(
            title,
            url,
            clean_text,
            "",
            category
        )


        print(
            "Saved:",
            article_id
        )


        return article_id




    def run(self, topic, limit=5):


        print(
            "Searching:",
            topic
        )


        urls = self.search.search(
            topic,
            limit
        )


        print(
            "Found:",
            len(urls),
            "articles"
        )


        results = []


        for url in urls:

            article_id = self.process_article(
                url
            )


            if article_id:

                results.append(
                    article_id
                )


        return results




    def process(self, topic, url=None):

        print(
            "Processing:",
            topic
        )


        if url:

            return self.process_article(
                url
            )


        return self.run(
            topic,
            5
        )



if __name__ == "__main__":


    pipeline = Pipeline()


    pipeline.run(
        "Artificial Intelligence",
        3
    )
