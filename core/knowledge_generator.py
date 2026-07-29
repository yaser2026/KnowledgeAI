from core.database import Database
from core.source_manager import SourceManager
from core.summarizer import Summarizer
from core.keyword_extractor import KeywordExtractor
from core.keyword_filter import KeywordFilter
from core.keyword_ranker import KeywordRanker


class KnowledgeGenerator:


    def __init__(self):

        self.database = Database()

        self.source_manager = SourceManager()

        self.summarizer = Summarizer()

        self.keyword_extractor = KeywordExtractor()

        self.keyword_filter = KeywordFilter()

        self.keyword_ranker = KeywordRanker()



    def get_articles_by_job(
        self,
        job_id
    ):

        self.database.cursor.execute(
            """
            SELECT
                id,
                title,
                url,
                content
            FROM articles
            WHERE job_id=?
            """,
            (
                job_id,
            )
        )

        return self.database.cursor.fetchall()



    def create_knowledge(
        self,
        topic,
        job_id
    ):


        articles = self.get_articles_by_job(
            job_id
        )


        if not articles:

            print(
                "No articles found for job"
            )

            return None



        combined = ""

        for article_id, title, url, content in articles:

            combined += "\n" + content



        summary = self.summarizer.summarize(
            combined,
            5
        )



        keywords = self.keyword_extractor.extract(
            combined,
            20
        )


        keywords = self.keyword_filter.filter(
            keywords
        )


        keywords = self.keyword_ranker.rank(
            keywords,
            10
        )



        title = (
            "Knowledge Report: "
            +
            topic
        )



        self.database.cursor.execute(
            """
            INSERT INTO knowledge_articles
            (
                topic,
                title,
                summary,
                content,
                keywords,
                job_id
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                topic,
                title,
                summary,
                combined,
                ", ".join(keywords),
                job_id
            )
        )


        self.database.conn.commit()


        knowledge_id = self.database.cursor.lastrowid



        print(
            "Knowledge created:",
            knowledge_id
        )



        print(
            "Saving sources..."
        )



        for article_id, source_title, url, content in articles:


            self.source_manager.add_source(

                knowledge_id,

                job_id,

                source_title,

                url
            )



        print(
            "Sources saved:",
            len(articles)
        )



        print(
            "Keywords:",
            keywords
        )



        return knowledge_id




if __name__ == "__main__":


    generator = KnowledgeGenerator()


    generator.create_knowledge(
        "Artificial Intelligence",
        6
    )
