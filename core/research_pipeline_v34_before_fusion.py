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

from core.snippet_extractor import SnippetExtractor
from core.query_focus import QueryFocus


class ResearchPipeline:


    def __init__(self):

        self.analyzer = QueryAnalyzer()

        self.search = SearchEngine()

        self.adapter = ResearchAdapter()

        self.source_diversity = SourceDiversity()

        self.reranker = ReRanker()


        self.evidence = EvidenceMerger()

        self.evidence_ranker = EvidenceRanker()

        self.confidence = ConfidenceEngine()


        self.query_focus = QueryFocus()

        self.snippet = SnippetExtractor()


        self.context = ContextBuilder()

        self.quality_filter = ContentQualityFilter()

        self.selector = SentenceSelector()


        self.citation = CitationManager()

        self.citation_dedup = CitationDeduplicator()


        self.answer = AnswerGenerator()

        self.synthesizer = AnswerSynthesizer()

        self.cleaner = AnswerCleaner()

        self.formatter = ResponseFormatter()



    def run(
        self,
        question,
        limit=5
    ):


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


        ranked_evidence = self.evidence_ranker.rank(
            merged
        )


        focused_evidence = self.query_focus.filter(
            ranked_evidence,
            question
        )


        for item in focused_evidence:

            text = item.get(
                "text",
                item.get(
                    "content",
                    ""
                )
            )


            snippets = self.snippet.extract(
                text,
                question
            )


            if snippets:

                item["text"] = " ".join(
                    snippets
                )


        filtered_evidence = self.quality_filter.filter(
            focused_evidence
        )


        confidence_score = self.confidence.calculate(
            filtered_evidence
        )


        context = self.context.build(
            filtered_evidence
        )


        selected = self.selector.select(
            filtered_evidence
        )


        print("\n===== DEBUG SELECTED =====")

        for item in selected:

            print(item)


        print("\n===== DEBUG CITATION INPUT =====")


        citations_raw = self.citation.format(
            selected
        )


        print(citations_raw)


        citations = self.citation_dedup.deduplicate(
            citations_raw.split("\n")
        )


        print("\n===== DEBUG FINAL CITATIONS =====")

        print(citations)



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

            "evidence": filtered_evidence,

            "confidence": confidence_score,

            "evidence_count": len(filtered_evidence),

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


    print("\n===== RESULT =====")


    print(
        "Confidence:",
        result["confidence"]
    )


    print(
        "Evidence:",
        result["evidence_count"]
    )


    print()


    for item in result["evidence"]:

        print(item)


    print()

    print(
        result["citations"]
    )
