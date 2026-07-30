class SourceAuthority:


    def __init__(self):

        self.rules = {

            "docs.kernel.org": 1.0,
            "kernel.org": 0.95,

            "github.com": 0.85,

            "redhat.com": 0.85,
            "ibm.com": 0.80,

            "microsoft.com": 0.80,

            "wikipedia.org": 0.70,

            "geeksforgeeks.org": 0.60,

        }



    def get_score(self, url):

        if not url:
            return 0.30


        url = url.lower()


        for domain, score in self.rules.items():

            if domain in url:

                return score


        return 0.30
