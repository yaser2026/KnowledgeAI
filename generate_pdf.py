from core.database import Database
from pdf.pdf_builder import PDFBuilder


class PDFGenerator:


    def __init__(self):

        self.database = Database()

        self.pdf = PDFBuilder()



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
            (article_id,)
        )


        article = self.database.cursor.fetchone()


        if not article:

            print("Article not found")

            return



        title, summary, keywords, content = article


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
            filename
        )



if __name__ == "__main__":


    generator = PDFGenerator()


    generator.generate(
        5
    )
