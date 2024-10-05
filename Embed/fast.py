# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel

# # Instantiate the class
# app = FastAPI()

# db = lancedb.connect("~/tmp/lancedbprj")

# table_name = "ProjectFiles"


# def get_context(query):
#     emb = embed_func(query)[0]
#     context = tbl.search(emb).limit(5).to_pandas()
#     return context
# tbl = db.open_table(table_name)

# # Define a GET method on the specified endpoint
# @app.get("/")
# def read_root():
#     return {"message": "Hello, FastAPI!"}


# @app.get("/get-context/{context}")
# def parse_gh(context):
#     return context
