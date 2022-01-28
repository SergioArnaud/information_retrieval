from elasticsearch import helpers, Elasticsearch


def connect():
    return Elasticsearch("localhost:9200")


def bulk_upsert(es, id_field, index, dicts, bool_parse=False, dateFormats=None):
    dicts_to_insert = []
    try:
        for i, dic in enumerate(dicts):
            # print(i)
            d = {}
            d["_id"] = dic[id_field]
            d["_index"] = index
            d["_op_type"] = "update"
            d["doc_as_upsert"] = True
            d["doc"] = dic
            dicts_to_insert.append(d)
            # print(d)
        helpers.bulk(es, dicts_to_insert)
    except Exception as ex:
        print("Failed to insert:" + str(ex))


def build_query(embedding, size, body={}):
    script_query = {
        "query": {
            "script_score": {
                "query": {"bool": {"must": [{"exists": {"field": "embedding"}}]}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, doc['embedding']) + 1.0",
                    "params": {"query_vector": embedding},
                },
            }
        },
    }

    return script_query


def create_index(es, index, mapping):
    if not es.indices.exists(index):
        es.indices.create(index, body=mapping)
