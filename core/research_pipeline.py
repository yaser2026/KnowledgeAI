from core.query_analyzer import QueryAnalyzer
from core.reranker import ReRanker
from core.context_builder import ContextBuilder
from core.citation import CitationManager
from core.answer_generator import AnswerGenerator
from core.research_adapter import ResearchAdapter
from core.search_engine import SearchEngine


class ResearchPipeline:


    def __init__(self):

        self.analyzer = QueryAnalyzer()
        self.search = SearchEngine()
        self.adapter = ResearchAdapter()
        self.reranker = ReRanker()
        self.context = ContextBuilder()
        self.citation = CitationManager()
        self.answer = AnswerGenerator()



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


        context = self.context.build(
            ranked
        )


        citations = self.citation.format(
            context["context"]
        )


        answer = self.answer.build_answer(
            question,
            context["context"],
            citations
        )


        return {
            "analysis": analysis,
            "answer": answer,
            "results": ranked,
            "context": context,
            "citations": citations
        }
