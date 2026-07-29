import re


class Cleaner:


    def clean(self, text):

        if not text:
            return ""


        # حذف فاصله‌های اضافی
        text = re.sub(
            r'\s+',
            ' ',
            text
        )


        # حذف فاصله ابتدا و انتها
        text = text.strip()


        # حذف کاراکترهای غیرضروری
        text = re.sub(
            r'[^\w\s.,;:!?()\[\]{}\-_/]',
            '',
            text,
            flags=re.UNICODE
        )


        return text



if __name__ == "__main__":


    cleaner = Cleaner()


    sample = """
    Hello      World!!!


    This is    KnowledgeAI.
    """


    result = cleaner.clean(sample)


    print(result)
