from core.query_analyzer import QueryAnalyzer
from core.reranker import ReRanker
from core.context_builder import ContextBuilder
from core.citation import CitationManager
from core.search_engine import SearchEngine


class ResearchPipeline:

    def __init__(self):

        self.analyzer = QueryAnalyzer()
        self.search = SearchEngine()
        self.reranker = ReRanker()
        self.context = ContextBuilder()
        self.citation = CitationManager()


    def run(self, question, limit=5):

        analysis = self.analyzer.analyze(
            question
        )


        results = self.search.search(
            question,
            limit
        )


        ranked = self.reranker.rerank(
            results
        )


        context = self.context.build(
            ranked
        )


        return {
            "analysis": analysis,
            "context": context
        }
