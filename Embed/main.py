import json
import os
import pathlib

import lancedb
import pandas as pd
import requests
from fastapi import FastAPI, HTTPException
from lancedb.context import contextualize
from lancedb.embeddings import with_embeddings
from parse_files import parse_files

db = lancedb.connect("~/tmp/lancedbprj")

table_name = "ProjectFiles"

pdf_urls = [
    "https://arxiv.org/pdf/2311.16863",
    "https://arxiv.org/pdf/2310.03003",
    "https://arxiv.org/pdf/2104.10350",
    "https://dl.acm.org/doi/pdf/10.1145/3610954",
]


def get_embed(s):
    url = "https://08eo1usy78.execute-api.us-west-2.amazonaws.com/titanEmbed"
    headers = {"Content-Type": "application/json"}
    payload = json.dumps({"query-string": s})
    response = requests.post(url, headers=headers, data=payload)
    body = json.loads(response.json()["body"])
    return body["embedding"]


def embed_func(c: str | list[str]):
    if isinstance(c, str):
        c = [c]
    return [get_embed(i) for i in c]


if table_name not in db.table_names():
    wd = os.getcwd()
    file_path = os.path.join(wd, "sus_files")
    paths = pathlib.Path(file_path)
    files = list(paths.rglob("*.pdf"))

    print("begin parsing")
    files_strings = []
    for f in files:
        files_strings.append(f.__str__())
    data = parse_files(files_strings)
    # print(len(data))
    df = (
        contextualize(pd.DataFrame({"text": data}))
        .text_col("text")
        .window(3)
        .stride(2)
        .to_pandas()
    )
    data = with_embeddings(embed_func, df, show_progress=True)
    print(data.to_pandas().head(1))
    tbl = db.create_table(table_name, data)
    print(f"Created LaneDB table of length: {len(tbl)}")
else:
    tbl = db.open_table(table_name)


def get_context(query):
    emb = embed_func(query)[0]
    context = tbl.search(emb).limit(5).to_pandas()
    return context


tbl = db.open_table(table_name)

app = FastAPI()


# Define a GET method on the specified endpoint
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


@app.get("/get-context/{query}")
def return_context(query):
    query = str(query)
    r = get_context(query)["text"].tolist()
    print(r)
    return r
