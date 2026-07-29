from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet
from pathlib import Path


class PDFBuilder:


    def __init__(self):

        self.output_dir = Path(
            "output"
        )

        self.output_dir.mkdir(
            exist_ok=True
        )



    def build(
        self,
        title,
        summary,
        keywords,
        content,
        filename
    ):


        path = (
            self.output_dir /
            filename
        )


        doc = SimpleDocTemplate(
            str(path)
        )


        styles = getSampleStyleSheet()

        story = []


        story.append(
            Paragraph(
                title,
                styles["Title"]
            )
        )

        story.append(
            Spacer(1, 12)
        )


        story.append(
            Paragraph(
                "<b>Summary</b>",
                styles["Heading2"]
            )
        )


        story.append(
            Paragraph(
                summary,
                styles["BodyText"]
            )
        )


        story.append(
            Spacer(1, 12)
        )


        story.append(
            Paragraph(
                "<b>Keywords</b>",
                styles["Heading2"]
            )
        )


        story.append(
            Paragraph(
                keywords,
                styles["BodyText"]
            )
        )


        story.append(
            Spacer(1, 12)
        )


        story.append(
            Paragraph(
                "<b>Content</b>",
                styles["Heading2"]
            )
        )


        story.append(
            Paragraph(
                content[:10000],
                styles["BodyText"]
            )
        )


        doc.build(
            story
        )


        print(
            "PDF created:",
            path
        )


if __name__ == "__main__":

    pdf = PDFBuilder()

    pdf.build(
        "Test Report",
        "This is summary",
        "AI, Machine Learning",
        "KnowledgeAI content",
        "test.pdf"
    )
