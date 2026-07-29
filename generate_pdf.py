from core.database import Database
from pdf.pdf_builder import PDFBuilder


class PDFGenerator:


    def __init__(self):

        self.database = Database()

        self.pdf = PDFBuilder()



    def get_sources(self, knowledge_id):

        self.database.cursor.execute(
            """
            SELECT
            title,
            url,
            domain,
            quality_score
            FROM knowledge_sources
            WHERE knowledge_id = ?
            """,
            (
                knowledge_id,
            )
        )


        rows = self.database.cursor.fetchall()


        sources = []


        for row in rows:

            sources.append(
                {
                    "title": row[0],
                    "url": row[1],
                    "domain": row[2],
                    "quality_score": row[3]
                }
            )


        return sources




    def generate(self, article_id):


        self.database.cursor.execute(
            """
            SELECT
            title,
            summary,
            keywords,
            content
            FROM knowledge_articles
            WHERE id = ?
            """,
            (
                article_id,
            )
        )


        article = self.database.cursor.fetchone()


        if not article:

            print(
                "Article not found"
            )

            return



        title, summary, keywords, content = article



        sources = self.get_sources(
            article_id
        )



        filename = (
            "Knowledge_Report_"
            +
            str(article_id)
            +
            ".pdf"
        )



        self.pdf.build(
            title,
            summary,
            keywords,
            content,
            filename,
            sources
        )



if __name__ == "__main__":


    generator = PDFGenerator()


    generator.generate(
        5
    )
