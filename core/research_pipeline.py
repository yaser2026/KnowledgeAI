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
from core.source_diversity import SourceDiversity
from core.search_engine import SearchEngine

from core.evidence_merger import EvidenceMerger
from core.evidence_ranker import EvidenceRanker
from core.confidence import ConfidenceEngine


class ResearchPipeline:

    def __init__(self):

        self.analyzer = QueryAnalyzer()

        self.search = SearchEngine()

        self.adapter = ResearchAdapter()

        self.source_diversity = SourceDiversity()

        self.reranker = ReRanker()

        self.evidence = EvidenceMerger()

        self.confidence = ConfidenceEngine()

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


        diverse = self.source_diversity.filter(
            ranked
        )


        merged = self.evidence.merge(
            diverse
        )

        merged = self.evidence_ranker.rank(
            merged
        )

        merged = self.evidence_ranker.rank(
            merged
        )


        confidence_score = self.confidence.calculate(
            merged
        )


        context = self.context.build(
            merged
        )


        filtered = self.quality_filter.filter(
            context["context"]
        )


        selected = self.selector.select(
            filtered
        )


        citations_raw = self.citation.format(
            selected
        )


        citations = self.citation_dedup.deduplicate(
            citations_raw.split("\n")
        )


        sentences = self.synthesizer.synthesize(
            selected
        )


        raw_answer = self.answer.build_answer(
            question,
            [
                {
                    "text": x
                }
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

            "results": diverse,

            "evidence": merged,

            "confidence": confidence_score,

            "evidence_count": len(merged),

            "context": context,

            "answer": response["answer"],

            "citations": response["citations"]

        }



if __name__ == "__main__":

    pipeline = ResearchPipeline()

    result = pipeline.run(
        "What is Linux kernel?",
        3
    )


    print(result["answer"])

    print()

    print("Confidence:",
          result["confidence"])

    print("Evidence:",
          result["evidence_count"])

    print()

    print(result["citations"])
