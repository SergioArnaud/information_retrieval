import os
import json
from information_retrieval.utils.elastic import connect, bulk_upsert, create_index
from information_retrieval import SemanticEmbedder


class Prepare():
    def __init__(self, file_folder, text_field, id_field, es_index):
        self.text_field = text_field
        self.file_folder = file_folder
        self.es = connect()
        self.es_index = es_index
        self.id_field = id_field
        self.retriever = SemanticEmbedder()

    def get_documents(self):
        self.documents = []
        for file in os.listdir(self.file_folder):
            if file.endswith(".json"):
                self.documents.extend(json.load(open(self.file_folder + file)))

    def add_embeddings(self):
        self.texts = [doc[self.text_field] for doc in self.documents]
        self.embeddings = self.retriever.embed(self.texts)
        for embeddding, doc in zip(self.embeddings, self.documents):
            doc["embedding"] = embeddding.tolist()

    def create_elastic_index(self):
        
        mapping = {
            "mappings": {
                "properties": {
                    "embedding": {"type": "dense_vector", "dims": 768},
                    self.text_field: {"type": "text"},
                }
            }
        }
        create_index(self.es, self.es_index, mapping)

    def upload_to_elastic(self):
        bulk_upsert(self.es, self.id_field, self.es_index, self.documents)

    def prepare(self):
        print("Preparing documents...")
        self.get_documents()

        print("Adding embeddings...")
        self.add_embeddings()

        print("Creating elastic index...")
        self.create_elastic_index()

        print("Uploading to elastic...")
        self.upload_to_elastic()
