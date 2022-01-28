## Main Idea

The following links explain a bit the idea of semantic search and how search mechanisms work by doing retrieve and rerank

- [Semantic Search](https://www.sbert.net/examples/applications/semantic-search/README.html)

- [Retrieve and Rerank](https://www.sbert.net/examples/applications/retrieve_rerank/README.html)

## Setup
## Download trained models

There are two models trained for spanish, a bi-encoder and a cross-encoder. These serve to make the retrieval system using the retrieve and rerank idea:

```
make setup
pip install -r requirements.txt
```


## Basic usage

1. Setup Elasticsearch index with semantic vectors. For this step we supose that a set of json files is folder. Each json can contain several optional fields but need to contain id and text fiedlds. 
```
from information_retrieval import SemanticEmbedder, CrossEncoder, Prepare, Search

data_folder = 'data/'
text_field = "texto_parrafo"
id_field = "id_parrafo"
elastic_index_name = "sentencias_2.0"

# Read the files, compute embeddings and upload them to elasticsearch
P = Prepare(data_folder, text_field, id_field, elastic_index_name)
P.prepare()
```

2. Make queries to retrieve documents:
```
from information_retrieval import SearchEngine

query = "la vida es bella"
S = SearchEngine(elastic_index_name)
S.retrieve(query) # Only semantic search

S.rerank(query) # Retrieve and rerank
```


## Model architecture


## Training

## Finetuning