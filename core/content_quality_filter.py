import re


class ContentQualityFilter:


    def __init__(self):
        pass


    def is_bad(self, text):

        if not text:
            return True


        length = len(text)


        if length < 40:
            return True


        # حذف جدول/مشخصات صفحه
        bad_patterns = [
            r"original author",
            r"stable release",
            r"preview release",
            r"website",
            r"repository",
            r"license",
            r"written in",
            r"------"
        ]


        lower = text.lower()


        for p in bad_patterns:
            if re.search(p, lower):
                return True


        # درصد علائم غیرطبیعی
        symbols = len(
            re.findall(
                r"[\[\]{}():]",
                text
            )
        )


        if symbols > 8:
            return True


        return False



    def filter(self, items):

        results = []


        for item in items:

            text = item.get(
                "text",
                ""
            )


            if not self.is_bad(text):

                results.append(
                    item
                )


        return results
