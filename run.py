from core.pipeline import Pipeline


def main():

    print("=" * 50)
    print("KnowledgeAI V1.0")
    print("=" * 50)


    topic = input(
        "Enter topic: "
    ).strip()


    if not topic:
        print("No topic entered")
        return


    print()
    print(
        "Processing:",
        topic
    )


    pipeline = Pipeline()


    pipeline.process(
        topic,
        "https://example.com"
    )



if __name__ == "__main__":
    main()
