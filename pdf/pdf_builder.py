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
        filename,
        sources=None,
        research=None
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



        # Title

        story.append(
            Paragraph(
                title,
                styles["Title"]
            )
        )


        story.append(
            Spacer(1,12)
        )



        # Research Score

        if research:


            story.append(
                Paragraph(
                    "<b>Research Quality</b>",
                    styles["Heading2"]
                )
            )


            research_text = (
                f"Overall Score: {research['score']}/100<br/>"
                f"Sources analyzed: {research['source_count']}<br/>"
                f"Articles analyzed: {research['article_count']}<br/>"
                f"Average source quality: "
                f"{research['average_quality']}/5"
            )


            story.append(
                Paragraph(
                    research_text,
                    styles["BodyText"]
                )
            )


            story.append(
                Spacer(1,12)
            )



        # Summary

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
            Spacer(1,12)
        )



        # Keywords

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
            Spacer(1,12)
        )



        # Content

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


        story.append(
            Spacer(1,12)
        )



        # References

        if sources:


            story.append(
                Paragraph(
                    "<b>References</b>",
                    styles["Heading2"]
                )
            )


            for index, source in enumerate(
                sources,
                1
            ):


                text = (
                    f"{index}. {source['title']}<br/>"
                    f"URL: {source['url']}<br/>"
                    f"Domain: {source['domain']}<br/>"
                    f"Quality Score: "
                    f"{source['quality_score']}/5"
                )


                story.append(
                    Paragraph(
                        text,
                        styles["BodyText"]
                    )
                )


                story.append(
                    Spacer(1,8)
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
        "test.pdf",
        [
            {
                "title": "Wikipedia",
                "url": "https://wikipedia.org",
                "domain": "wikipedia.org",
                "quality_score": 5
            }
        ],
        {
            "score":100,
            "source_count":1,
            "article_count":1,
            "average_quality":5
        }
    )
