import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "data" / "knowledge.db"



class Database:


    def __init__(self):

        self.conn = sqlite3.connect(
            DB_PATH
        )

        self.cursor = self.conn.cursor()



    def close(self):

        self.conn.close()



    # -------------------------
    # Jobs
    # -------------------------

    def create_job(
        self,
        query
    ):

        self.cursor.execute(
            """
            INSERT INTO jobs
            (
                query,
                status
            )
            VALUES (?, ?)
            """,
            (
                query,
                "running"
            )
        )

        self.conn.commit()

        return self.cursor.lastrowid



    def update_job_status(
        self,
        job_id,
        status
    ):

        self.cursor.execute(
            """
            UPDATE jobs
            SET status=?
            WHERE id=?
            """,
            (
                status,
                job_id
            )
        )

        self.conn.commit()



    def get_job(
        self,
        job_id
    ):

        self.cursor.execute(
            """
            SELECT *
            FROM jobs
            WHERE id=?
            """,
            (
                job_id,
            )
        )

        return self.cursor.fetchone()



    # -------------------------
    # Articles
    # -------------------------

    def add_article(
        self,
        title,
        url,
        content="",
        summary="",
        category="",
        job_id=None
    ):


        existing = self.get_by_url(
            url
        )


        if existing:


            self.cursor.execute(
                """
                UPDATE articles
                SET
                    title=?,
                    content=?,
                    summary=?,
                    category=?,
                    job_id=?,
                    created_at=CURRENT_TIMESTAMP
                WHERE url=?
                """,
                (
                    title,
                    content,
                    summary,
                    category,
                    job_id,
                    url
                )
            )


            self.conn.commit()


            print(
                "Article updated:",
                existing[0]
            )


            return existing[0]



        try:


            self.cursor.execute(
                """
                INSERT INTO articles
                (
                    title,
                    url,
                    content,
                    summary,
                    category,
                    job_id
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    title,
                    url,
                    content,
                    summary,
                    category,
                    job_id
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




    def get_by_url(
        self,
        url
    ):

        self.cursor.execute(
            """
            SELECT *
            FROM articles
            WHERE url=?
            """,
            (
                url,
            )
        )

        return self.cursor.fetchone()



    def get_article(
        self,
        article_id
    ):

        self.cursor.execute(
            """
            SELECT *
            FROM articles
            WHERE id=?
            """,
            (
                article_id,
            )
        )

        return self.cursor.fetchone()



    def get_articles_by_job(
        self,
        job_id
    ):

        self.cursor.execute(
            """
            SELECT title, content
            FROM articles
            WHERE job_id=?
            """,
            (
                job_id,
            )
        )

        return self.cursor.fetchall()



    def search_articles(
        self,
        keyword
    ):

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



    # -------------------------
    # Keywords
    # -------------------------

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



    # -------------------------
    # Logs
    # -------------------------

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


    job = db.create_job(
        "Database Test"
    )


    print(
        "Job ID:",
        job
    )


    db.update_job_status(
        job,
        "completed"
    )


    print(
        db.get_job(job)
    )


    db.close()
