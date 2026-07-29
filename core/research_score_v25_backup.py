from core.database import Database


class ResearchScore:


    def __init__(self):

        self.database = Database()



    def calculate(self, knowledge_id):

        cur = self.database.cursor


        # تعداد منابع
        cur.execute(
            """
            SELECT COUNT(*)
            FROM knowledge_sources
            WHERE knowledge_id=?
            """,
            (
                knowledge_id,
            )
        )

        source_count = cur.fetchone()[0]



        # تعداد مقاله‌ها
        cur.execute(
            """
            SELECT COUNT(*)
            FROM articles
            WHERE job_id=
            (
                SELECT job_id
                FROM knowledge_articles
                WHERE id=?
            )
            """,
            (
                knowledge_id,
            )
        )

        article_count = cur.fetchone()[0]



        # میانگین کیفیت منابع
        cur.execute(
            """
            SELECT AVG(quality_score)
            FROM knowledge_sources
            WHERE knowledge_id=?
            """,
            (
                knowledge_id,
            )
        )

        avg_quality = cur.fetchone()[0]


        if avg_quality is None:

            avg_quality = 0



        # امتیاز نهایی
        score = int(
            min(
                100,
                (
                    source_count * 10
                    +
                    article_count * 10
                    +
                    avg_quality * 10
                )
            )
        )



        # ذخیره یا بروزرسانی امتیاز
        cur.execute(
            """
            INSERT INTO research_scores
            (
                knowledge_id,
                source_count,
                article_count,
                average_quality,
                score
            )
            VALUES (?, ?, ?, ?, ?)

            ON CONFLICT(knowledge_id)
            DO UPDATE SET

                source_count=excluded.source_count,

                article_count=excluded.article_count,

                average_quality=excluded.average_quality,

                score=excluded.score,

                created_at=CURRENT_TIMESTAMP
            """,
            (
                knowledge_id,
                source_count,
                article_count,
                avg_quality,
                score
            )
        )


        self.database.conn.commit()



        return {

            "knowledge_id": knowledge_id,

            "sources": source_count,

            "articles": article_count,

            "average_quality": round(avg_quality, 2),

            "score": score

        }




if __name__ == "__main__":


    rs = ResearchScore()


    print(
        rs.calculate(12)
    )
