from urllib.parse import urlparse

from core.summarizer import Summarizer
from core.keyword_extractor import KeywordExtractor
from core.keyword_filter import KeywordFilter
from core.keyword_ranker import KeywordRanker
from core.database import Database
from core.source_manager import SourceManager


class KnowledgeGenerator:


    def __init__(self):

        self.summarizer = Summarizer()

        self.keyword_extractor = KeywordExtractor()

        self.keyword_filter = KeywordFilter()

        self.keyword_ranker = KeywordRanker()

        self.database = Database()

        self.source_manager = SourceManager()



    def get_articles(self, topic):

        self.database.cursor.execute(
            """
            SELECT id, title, url, content
            FROM articles
            WHERE title LIKE ?
            OR content LIKE ?
            """,
            (
                f"%{topic}%",
                f"%{topic}%"
            )
        )

        return self.database.cursor.fetchall()



    def create_knowledge(self, topic):

        articles = self.get_articles(topic)


        if not articles:

            print(
                "No articles found"
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
                keywords
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                topic,
                title,
                summary,
                combined,
                ", ".join(keywords)
            )
        )


        self.database.conn.commit()


        knowledge_id = self.database.cursor.lastrowid



        # ذخیره منابع گزارش

        for article_id, article_title, url, content in articles:

            if url:

                self.source_manager.add_source(
                    knowledge_id,
                    article_title,
                    url
                )



        print(
            "Knowledge created:",
            knowledge_id
        )


        print(
            "Keywords:",
            keywords
        )


        print(
            "Sources saved:",
            len(articles)
        )


        return knowledge_id



if __name__ == "__main__":

    generator = KnowledgeGenerator()

    generator.create_knowledge(
        "Artificial Intelligence"
    )
