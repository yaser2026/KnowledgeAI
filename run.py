from core.pipeline import Pipeline
from core.knowledge_generator import KnowledgeGenerator
from generate_pdf import PDFGenerator


def main():

    print("=" * 50)
    print("KnowledgeAI V2.1")
    print("=" * 50)


    topic = input(
        "Enter topic: "
    ).strip()


    if not topic:

        print(
            "No topic entered"
        )

        return



    print()

    print(
        "Collecting articles for:",
        topic
    )


    pipeline = Pipeline()


    articles = pipeline.process(
        topic
    )


    if not articles:

        print(
            "No articles collected"
        )

        return



    print()

    print(
        "Generating knowledge..."
    )


    generator = KnowledgeGenerator()


    knowledge_id = generator.create_knowledge(
        topic
    )


    if not knowledge_id:

        print(
            "Knowledge generation failed"
        )

        return



    print()

    print(
        "Generating PDF..."
    )


    pdf = PDFGenerator()


    pdf.generate(
        knowledge_id
    )


    print()

    print("=" * 50)
    print("KnowledgeAI completed successfully")
    print("=" * 50)



if __name__ == "__main__":

    main()
