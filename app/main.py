import asyncio
from typing import Dict, Optional, Union

from fastapi import FastAPI, HTTPException, Request
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel


from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles


class Account(BaseModel):
    name: str
    description: Optional[str] = None
    balance: float
    active: bool = True


app = FastAPI(docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory="static"), name="static")

accounts = dict()

async def get_account(account_id: int) -> Optional[Account]:
    if account_id in accounts:
        return accounts[account_id]
    else:
        return None

async def add_account(account_id: int, account: Account) -> Optional[Account]:
    if account_id in accounts:
        return None
    else:
        accounts[account_id] = account.dict()
        return accounts[account_id]

async def update_account(accoutn_id: int, account: Account) -> Optional[Account]:
    pass

async def delete_account(account_id: int) -> Optional[bool]:
    if account_id in accounts:
        return True
    else:
        return None


@app.get("/healthz")
async def get_health(request: Request) -> Union[Optional[Dict], HTTPException]:
    return {"status": True}

@app.get("/accounts/{account_id}")
async def read_account(account_id: int, status_code=200):
    res = await get_account(account_id)
    if res is None:
        raise HTTPException(status_code=404, detail="Account not found")
    else:
        return res

@app.put("/accounts/{account_id}", status_code=200)
async def update_account(account_id: int, account: Account):
    res = await get_account(account_id)
    if res is None:
        raise add_account(account_id, account)
    else:
        return await add_account(account_id, account)

@app.post("/accounts", status_code=200)
async def create_account(account_id: int, account: Account):
    res = await add_account(account_id, account)
    if res is None:
        raise HTTPException(status_code=409, detail="Account exists")
    else:
        return res

@app.delete("/accounts/{account_id}", status_code=200)
async def remove_account(deleted: Optional[bool]):
    if deleted is None:
        raise HTTPException(status_code=404, detail="Account not found")
    else:
        return {"msg": "Successful"}

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )

@app.get("/openapi", include_in_schema=False)
async def custom_swagger_ui_html():
    openapi_schema = get_openapi(
        title="API Specs",
        version="3.0.0",
        routes=app.routes,
    )
    return openapi_schema

