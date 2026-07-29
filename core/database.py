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

        except sqlite3.IntegrityError:
            return None


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
            SELECT id,title,category
            FROM articles
            WHERE content LIKE ?
            OR title LIKE ?
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

        self.cursor.execute(
            """
            INSERT INTO keywords
            (
                article_id,
                keyword
            )
            VALUES (?,?)
            """,
            (
                article_id,
                keyword
            )
        )

        self.conn.commit()


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
            VALUES (?,?)
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
        "Test Article",
        "https://example.com",
        "KnowledgeAI test content",
        "test summary",
        "AI"
    )

    print("Article ID:", article_id)

    print(
        db.search_articles("KnowledgeAI")
    )

    db.close()
