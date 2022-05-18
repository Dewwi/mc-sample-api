import asyncio
from typing import Dict, Optional, Union
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, HTTPException, Request
from .models import AccountBase


from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles

app = FastAPI(docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory="static"), name="static")

accounts = dict()

async def get_max_account_id() -> int:
    if not accounts:
        return 0
    else:
        return max(accounts)

async def get_account(account_id: int, accounts: Dict) -> Optional[AccountBase]:
    if account_id in accounts:
        return accounts[account_id]
    else:
        return None

async def account_exists(account_id: int, accounts: Dict) -> bool:
    if account_id in accounts:
        return True
    else:
        return False

async def add_replace_account(account: AccountBase, account_id: int = None) -> Optional[AccountBase]:
    if(account_id is None):
        account_id = await get_max_account_id() + 1
    accounts[account_id] = account.dict()
    return account_id, accounts[account_id]

async def delete_account(account_id: int) -> Optional[bool]:
    if account_id in accounts:
        return True
    else:
        return None


# ROUTES

@app.get("/healthz")
async def get_health(request: Request) -> Union[Optional[Dict], HTTPException]:
    """
    GET - Returns True is service is up
    """
    return {"status": True}

@app.get("/accounts/{account_id}")
async def read_account(account_id: int, status_code=200) -> Union[Optional[Dict], HTTPException]:
    """
    GET - Return dict for a given account ID, 404 if not found
    """
    res = await get_account(account_id, accounts)
    if res is None:
        raise HTTPException(status_code=404, detail="Account not found")
    else:
        return {'id': account_id, 'account': res}

@app.put("/accounts/{account_id}", status_code=200)
async def insert_or_replace_account(account_id: int, account: AccountBase) -> Union[Optional[Dict], HTTPException]:
    """
    PUT - Insert or replace account
    """
    account_id, res = await add_replace_account(account, account_id)
    return {'id': account_id, 'account': res}

@app.patch("/accounts/{account_id}", status_code=200)
async def update_account(account_id: int, account: AccountBase) -> Union[Optional[Dict], HTTPException]:
    """
    PATCH - Update account
    """
    exists = await account_exists(account_id, accounts)
    if(not exists):
        raise HTTPException(status_code=404, detail="Account not found")
    else:
        stored_account = accounts[account_id]
        stored_account_model = AccountBase(**stored_account)
        update_account_data = account.dict(exclude_unset=True)
        updated_account = stored_account_model.copy(update=update_account_data)
        accounts[account_id] = jsonable_encoder(updated_account)
    return {'id': account_id, 'account': updated_account}

@app.post("/accounts", status_code=200)
async def create_account(account: AccountBase = None) -> Union[Optional[Dict], HTTPException]:
    """
    POST - Create empty or non empty account and auto-assign an account ID
    """
    account_id, res = await add_replace_account(AccountBase(), None)
    return {'id': account_id, 'account': res}

@app.delete("/accounts/{account_id}", status_code=200)
async def remove_account(account_id:int) -> Union[Optional[Dict], HTTPException]:
    """
    DELETE - remove account 
    """
    exists = await account_exists(account_id, accounts)
    if exists:
        try:
            accounts.pop(account_id)
            return {"msg": "Successful"}
        except Exception as e:
            raise HTTPException(status_code=500, detail="Delete failed")
    else:
        raise HTTPException(status_code=404, detail="Account not found")
        

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    """
    GET - Serves SWAGGER UI Specs
    """
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )

