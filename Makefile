setup:
	curl https://deep-dive-data-science.s3.us-west-2.amazonaws.com/models/semantic_search_model.zip --output semantic_search_model.zip
	unzip semantic_search_model.zip information_retrieval/models/semantic_search_model
	rm semantic_search_model.zip

	curl https://deep-dive-data-science.s3.us-west-2.amazonaws.com/models/cross_encoder.zip --output cross_encoder.zip
	unzip cross_encoder.zip information_retrieval/models/cross_encoder_model
	rm cross_encoder.zip
