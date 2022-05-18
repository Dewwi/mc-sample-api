# Sample API

## Usage

### Dev environment

1 - `make install`
2 - `uvicorn app.main:app --reload`

### Docker

 1 - `make docker-build `
 2 - `make docker-run`
 
 ### Tests 
 
 1 - `make test`

## Generate OpenAPI Specs

### Swagger UI available via /docs

The specs are generated based of the source code and updated dynamically.

Run the app 
1 - `make docker-run` 
2 - open http://localhost:80/docs in your browser

### Generate Markdown version using widdershins

1 - `python app/generate_specs.py`
2 - `widdershins specs/openapi.json -o specs/openapi.md`

OR 

1 - `make generate-md-specs`





