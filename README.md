# Sample API

## Usage

### Dev environment

- `make install`
- `uvicorn app.main:app --reload`

### Docker

 - `make docker-build `
 - `make docker-run`
 
### Tests 
 
- `make test`

## Generate OpenAPI Specs

### Swagger UI available via /docs

The specs are generated based of the source code and updated dynamically.

Run the app 
- `make docker-run` 
- open http://localhost:80/docs in your browser

### Generate Markdown version using widdershins

- `python app/generate_specs.py`
- `widdershins specs/openapi.json -o specs/openapi.md`

OR 

- `make generate-md-specs`





