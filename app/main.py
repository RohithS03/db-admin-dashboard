from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.database import get_tables, get_table_schema, get_table_data, execute_raw_sql
import os

app = FastAPI(title="DB Admin Dashboard")

templates_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")

templates = Jinja2Templates(directory=templates_dir)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

from app.auth import get_current_username
from fastapi import Depends

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, username: str = Depends(get_current_username)):
    tables = get_tables()
    return templates.TemplateResponse("index.html", {"request": request, "tables": tables})

@app.get("/table/{table_name}", response_class=HTMLResponse)
async def view_table(request: Request, table_name: str, username: str = Depends(get_current_username)):
    tables = get_tables()
    columns, rows = get_table_data(table_name)
    schema = get_table_schema(table_name)
    return templates.TemplateResponse("table.html", {
        "request": request, "tables": tables, "table_name": table_name,
        "columns": columns, "rows": rows, "schema": schema
    })

@app.get("/query", response_class=HTMLResponse)
async def query_page(request: Request, username: str = Depends(get_current_username)):
    tables = get_tables()
    return templates.TemplateResponse("query.html", {"request": request, "tables": tables, "query": "", "error": None, "columns": [], "rows": []})

@app.post("/query", response_class=HTMLResponse)
async def run_query(request: Request, sql_query: str = Form(...), username: str = Depends(get_current_username)):
    tables = get_tables()
    columns, rows, error = execute_raw_sql(sql_query)
    return templates.TemplateResponse("query.html", {
        "request": request, "tables": tables, "query": sql_query,
        "error": error, "columns": columns, "rows": rows
    })
