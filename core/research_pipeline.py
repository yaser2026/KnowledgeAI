from core.query_analyzer import QueryAnalyzer
from core.reranker import ReRanker
from core.context_builder import ContextBuilder

from core.citation import CitationManager
from core.citation_deduplicator import CitationDeduplicator

from core.answer_generator import AnswerGenerator
from core.answer_synthesizer import AnswerSynthesizer
from core.answer_cleaner import AnswerCleaner
from core.response_formatter import ResponseFormatter

from core.sentence_selector import SentenceSelector
from core.content_quality_filter import ContentQualityFilter

from core.research_adapter import ResearchAdapter
from core.search_engine import SearchEngine


class ResearchPipeline:

    def __init__(self):

        self.analyzer = QueryAnalyzer()

        self.search = SearchEngine()
        self.adapter = ResearchAdapter()

        self.reranker = ReRanker()

        self.context = ContextBuilder()

        self.quality_filter = ContentQualityFilter()
        self.selector = SentenceSelector()

        self.citation = CitationManager()
        self.citation_dedup = CitationDeduplicator()

        self.answer = AnswerGenerator()
        self.synthesizer = AnswerSynthesizer()

        self.cleaner = AnswerCleaner()
        self.formatter = ResponseFormatter()


    def run(self, question, limit=5):

        analysis = self.analyzer.analyze(
            question
        )


        urls = self.search.search(
            question,
            limit
        )


        results = self.adapter.convert(
            urls
        )


        ranked = self.reranker.rerank(
            results
        )


        context = self.context.build(
            ranked
        )


        filtered = self.quality_filter.filter(
            context["context"]
        )


        selected = self.selector.select(
            filtered
        )


        # citation generation

        citations_raw = self.citation.format(
            selected
        )


        citations = self.citation_dedup.deduplicate(
            citations_raw.split("\n")
        )


        # answer synthesis

        sentences = self.synthesizer.synthesize(
            selected
        )


        raw_answer = self.answer.build_answer(
            question,
            [
                {"text": x}
                for x in sentences
            ],
            "\n".join(citations)
        )


        clean_answer = self.cleaner.clean(
            raw_answer
        )


        response = self.formatter.format(
            clean_answer,
            citations
        )


        return {

            "analysis": analysis,

            "results": ranked,

            "context": context,

            "answer": response["answer"],

            "citations": response["citations"]

        }


if __name__ == "__main__":

    p = ResearchPipeline()

    r = p.run(
        "What is Linux kernel?",
        3
    )

    print(r["answer"])
    print()
    print(r["citations"])
