import requests
import time


class Downloader:


    def __init__(self):

        self.session = requests.Session()

        self.session.headers.update(
            {
                "User-Agent":
                "Mozilla/5.0 (Linux; Android 11) "
                "AppleWebKit/537.36 "
                "Chrome/120 Mobile Safari/537.36",

                "Accept-Language":
                "en-US,en;q=0.9"
            }
        )



    def download(
        self,
        url,
        retries=3
    ):


        for attempt in range(retries):

            try:

                response = self.session.get(
                    url,
                    timeout=20
                )


                if response.status_code == 403:

                    print(
                        "Access denied:",
                        url
                    )

                    return None



                response.raise_for_status()


                return response.text



            except Exception as e:

                print(
                    f"Download attempt {attempt+1} failed:",
                    e
                )


                time.sleep(2)



        return None



if __name__ == "__main__":


    downloader = Downloader()


    html = downloader.download(
        "https://example.com"
    )


    if html:
        print(html[:200])
