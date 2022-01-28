from information_retrieval.utils.elastic import connect, build_query
from information_retrieval import SemanticEmbedder, CrossEncoder

class Search():
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
    
    def re_rank(self, question, size=5):
        res = self.retrieve(question, size)
        scores = []
        for hit in res:
            scores.append((hit["_score"], hit["_source"]["embedding"]))
        scores = sorted(scores, key=lambda x: x[0], reverse=True)
        return scores