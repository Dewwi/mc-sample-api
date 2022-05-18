.PHONY: 

help: 
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:
	python3 -m venv venv
	source venv/bin/activate
	python -m pip install -r requirements.txt
	npm install -g widdershins.

generate-md-specs:
	python app/generate_specs.py
	widdershins specs/openapi.json -o specs/openapi.md

test: 
	pytest

docker-build:
	docker build -t sample_app .

docker-run:
	docker run -dp 80:80 sample_app
	open http://localhost:80/docs

