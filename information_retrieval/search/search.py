from information_retrieval.utils.elastic import connect, build_query
from information_retrieval import SemanticEmbedder, CrossEncoder


class SearchEngine:
    def __init__(self, es_index):
        self.es = connect()
        self.es_index = es_index
        self.retriever = SemanticEmbedder()
        self.re_ranker = CrossEncoder()

    def retrieve(self, query, size=5):
        query_embedding = self.retriever.embed(query)
        body = build_query(query_embedding, size)
        res = self.es.search(index=self.es_index, body=body, size=size)
        return res["hits"]["hits"]

    def rerank(self, question, size=5):
        raise NotImplementedError

    def retrieve_and_rerank(self, question, retrieval_size=30, rerank_size=5):
        raise NotImplementedError
