from urllib.parse import urlparse
from core.database import Database


class SourceManager:


    def __init__(self):

        self.database = Database()



    def quality_score(self, url):

        domain = urlparse(url).netloc.lower()


        trusted = {

            "wikipedia.org": 5,

            "nist.gov": 5,

            "ibm.com": 5,

            "nature.com": 5,

            "scientificamerican.com": 4,

            "geeksforgeeks.org": 3

        }


        for site, score in trusted.items():

            if site in domain:

                return score


        return 2



    def add_source(
        self,
        knowledge_id,
        title,
        url
    ):


        domain = urlparse(url).netloc


        score = self.quality_score(
            url
        )


        self.database.cursor.execute(
            """
            INSERT INTO knowledge_sources
            (
                knowledge_id,
                title,
                url,
                domain,
                quality_score
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                knowledge_id,
                title,
                url,
                domain,
                score
            )
        )


        self.database.conn.commit()


        return self.database.cursor.lastrowid



if __name__ == "__main__":

    manager = SourceManager()


    print(
        manager.quality_score(
            "https://www.nist.gov/quantum"
        )
    )
