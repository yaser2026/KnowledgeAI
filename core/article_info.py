from bs4 import BeautifulSoup


class ArticleInfo:


    def extract(self, html):

        if not html:
            return {}


        soup = BeautifulSoup(
            html,
            "lxml"
        )


        title = ""


        if soup.title:

            title = soup.title.text.strip()



        return {
            "title": title
        }



if __name__ == "__main__":

    html = """
    <html>
    <title>Artificial Intelligence</title>
    </html>
    """


    info = ArticleInfo()


    print(
        info.extract(html)
    )
