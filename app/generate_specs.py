from main import app
from fastapi.openapi.utils import get_openapi
import json


openapi_schema = get_openapi(
        title="API Specs",
        version="3.0.0",
        routes=app.routes,
)

with open('specs/openapi.json', 'w') as outfile:
        json.dump(openapi_schema, outfile)