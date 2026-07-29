import re


class ContentQualityFilter:


    def __init__(self):
        pass



    def is_bad(self, text):

        if not text:
            return True


        text = text.strip()


        if len(text) < 80:
            return True



        lower = text.lower()



        bad_patterns = [
            "about contact",
            "site news",
            "atom feed",
            "mailing lists",
            "patchwork",
            "mirrors",
            "social site",
            "faq",
            "bugzilla"
        ]


        for p in bad_patterns:

            if p in lower:
                return True



        # حذف متن‌هایی که بیشتر شبیه منو هستند

        words = text.split()


        if len(words) > 0:

            unique_ratio = len(
                set(words)
            ) / len(words)


            if unique_ratio < 0.35:
                return True



        # حذف متن با لینک/نشانه زیاد

        symbols = len(
            re.findall(
                r'[/|@:_-]',
                text
            )
        )


        if symbols > 12:
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
