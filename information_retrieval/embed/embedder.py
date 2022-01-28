from torch.nn import functional as F
import torch
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import BertForSequenceClassification, XLMRobertaTokenizer


class SemanticEmbedder:
    def __init__(
        self, semantic_model="information_retrieval/models/semantic_search_model", verbose=True, batch_size=32
    ):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.retriever_model = semantic_model
        self.verbose = verbose
        self.batch_size = batch_size
        self.retriever = SentenceTransformer(self.retriever_model, device=device)

    def embed(self, sentences):
        return self.retriever.encode(
            sentences, batch_size=self.batch_size, show_progress_bar=self.verbose
        )


class CrossEncoder:
    def __init__(self, cross_encoder_model="information_retrieval/models/cross_encoder_model"):
        self.tokenizer = XLMRobertaTokenizer.from_pretrained(cross_encoder_model)
        self.model = BertForSequenceClassification.from_pretrained(cross_encoder_model)

    def __prepare(self, sentences, query):
        list_questions = [{"question": query, "context": text} for text in sentences]
        questions = [r["question"] for r in list_questions]
        context = [r["context"][:512] for r in list_questions]
        return questions, context

    def score(self, sentences, query):
        questions, context = self.__prepare(sentences, query)
        features = self.tokenizer(
            questions, context, padding=True, truncation=True, return_tensors="pt"
        )
        self.model.eval()
        with torch.no_grad():
            scores = self.model(**features).logits

        results_sorted = sorted(
            list(zip(scores, context)), key=lambda x: x[0], reverse=True
        )
        return results_sorted
