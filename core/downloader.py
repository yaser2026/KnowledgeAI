import requests


class Downloader:

    def __init__(self):
        self.headers = {
            "User-Agent":
            "Mozilla/5.0"
        }


    def download(self, url):

        try:

            response = requests.get(
                url,
                headers=self.headers,
                timeout=15
            )

            response.raise_for_status()

            return response.text

        except Exception as e:

            print("Download error:", e)

            return None



if __name__ == "__main__":

    downloader = Downloader()

    html = downloader.download(
        "https://example.com"
    )

    if html:
        print(
            html[:200]
        )
