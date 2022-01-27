download_models:
	curl https://deep-dive-data-science.s3.us-west-2.amazonaws.com/models/semantic_search_model.zip --output semantic_search_model.zip
	unzip semantic_search_model.zip
	rm semantic_search_model.zip

	curl https://deep-dive-data-science.s3.us-west-2.amazonaws.com/models/cross_encoder.zip --output cross_encoder.zip
	unzip cross_encoder.zip
	rm cross_encoder.zip