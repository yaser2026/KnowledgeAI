from urllib.parse import urlparse


class SourceDiversity:

    def __init__(self, max_per_domain=1):
        self.max_per_domain = max_per_domain


    def get_domain(self, url):

        if not url:
            return ""

        try:
            domain = urlparse(url).netloc

            return domain.replace(
                "www.",
                ""
            )

        except Exception:
            return ""


    def filter(self, results):

        selected = []

        domain_count = {}

        for item in results:

            domain = self.get_domain(
                item.get("url", "")
            )

            if not domain:
                continue


            count = domain_count.get(
                domain,
                0
            )


            if count < self.max_per_domain:

                selected.append(item)

                domain_count[domain] = count + 1


        return selected
