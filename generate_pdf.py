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




    def get_research_score(self, knowledge_id):

        self.database.cursor.execute(
            """
            SELECT
                source_count,
                article_count,
                average_quality,
                score
            FROM research_scores
            WHERE knowledge_id = ?
            """,
            (
                knowledge_id,
            )
        )


        row = self.database.cursor.fetchone()


        if not row:

            return {

                "source_count": 0,

                "article_count": 0,

                "average_quality": 0,

                "score": 0
            }



        return {

            "source_count": row[0],

            "article_count": row[1],

            "average_quality": row[2],

            "score": row[3]

        }




    def generate(self, knowledge_id):


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
                knowledge_id,
            )
        )


        article = self.database.cursor.fetchone()


        if not article:

            print(
                "Knowledge article not found"
            )

            return



        title, summary, keywords, content = article



        sources = self.get_sources(
            knowledge_id
        )


        research = self.get_research_score(
            knowledge_id
        )



        filename = (
            "Knowledge_Report_"
            +
            str(knowledge_id)
            +
            ".pdf"
        )



        self.pdf.build(
            title,
            summary,
            keywords,
            content,
            filename,
            sources,
            research
        )


        print(
            "PDF created:",
            filename
        )




if __name__ == "__main__":


    generator = PDFGenerator()


    generator.generate(
        12
    )
