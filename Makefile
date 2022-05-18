.PHONY: all plan apply destroy

all: help

help: 
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:
	python3 -m venv venv
	source venv/bin/activate
	python3 -m pip install -r requirements.txt
	npm install -g widdershins.

test: check-var-env
	pytest

build:
	docker build -t sample_app .

run:
	docker run -p 80:80 sample_app

