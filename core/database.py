import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "data" / "knowledge.db"


class Database:

    def __init__(self):

        self.conn = sqlite3.connect(DB_PATH)

        self.cursor = self.conn.cursor()


    def close(self):

        self.conn.close()



    def add_article(
        self,
        title,
        url,
        content="",
        summary="",
        category=""
    ):

        existing = self.get_by_url(url)


        # اگر مقاله وجود داشت، بروزرسانی شود
        if existing:

            self.cursor.execute(
                """
                UPDATE articles
                SET
                    title=?,
                    content=?,
                    summary=?,
                    category=?,
                    created_at=CURRENT_TIMESTAMP
                WHERE url=?
                """,
                (
                    title,
                    content,
                    summary,
                    category,
                    url
                )
            )

            self.conn.commit()

            print(
                "Article updated:",
                existing[0]
            )

            return existing[0]



        # اگر جدید بود، ذخیره شود
        try:

            self.cursor.execute(
                """
                INSERT INTO articles
                (
                    title,
                    url,
                    content,
                    summary,
                    category
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    title,
                    url,
                    content,
                    summary,
                    category
                )
            )

            self.conn.commit()

            return self.cursor.lastrowid


        except sqlite3.Error as e:

            print(
                "Database error:",
                e
            )

            return None



    def get_by_url(self, url):

        self.cursor.execute(
            """
            SELECT *
            FROM articles
            WHERE url=?
            """,
            (url,)
        )

        return self.cursor.fetchone()



    def get_article(self, article_id):

        self.cursor.execute(
            """
            SELECT *
            FROM articles
            WHERE id=?
            """,
            (article_id,)
        )

        return self.cursor.fetchone()



    def search_articles(self, keyword):

        self.cursor.execute(
            """
            SELECT id, title, category
            FROM articles
            WHERE title LIKE ?
            OR content LIKE ?
            """,
            (
                f"%{keyword}%",
                f"%{keyword}%"
            )
        )

        return self.cursor.fetchall()



    def add_keyword(
        self,
        article_id,
        keyword
    ):

        try:

            self.cursor.execute(
                """
                INSERT INTO keywords
                (
                    article_id,
                    keyword
                )
                VALUES (?, ?)
                """,
                (
                    article_id,
                    keyword
                )
            )

            self.conn.commit()


        except sqlite3.Error as e:

            print(
                "Keyword error:",
                e
            )



    def add_log(
        self,
        action,
        message
    ):

        self.cursor.execute(
            """
            INSERT INTO logs
            (
                action,
                message
            )
            VALUES (?, ?)
            """,
            (
                action,
                message
            )
        )

        self.conn.commit()



if __name__ == "__main__":

    db = Database()


    article_id = db.add_article(
        "KnowledgeAI Test",
        "https://test.com",
        "Database manager test",
        "test summary",
        "AI"
    )


    print(
        "Article ID:",
        article_id
    )


    print(
        db.search_articles("KnowledgeAI")
    )


    db.close()
