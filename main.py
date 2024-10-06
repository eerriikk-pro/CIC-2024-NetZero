import json

import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ec2_gh.main import download_github_repo, get_repo_info


def get_suggestion(description):
    url = "https://l14zwywvx0.execute-api.us-west-2.amazonaws.com/suggest"

    payload = json.dumps({"description": description})
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url, headers=headers, data=payload)
    return response


# Instantiate the class
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Adjust to specify allowed origins (e.g., ["https://example.com"])
    allow_credentials=True,
    allow_methods=["*"],  # This allows all HTTP methods, including OPTIONS
    allow_headers=["*"],  # Allows all headers to be sent from the client
)


# Define a GET method on the specified endpoint
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


class GHLink(BaseModel):
    gh_link: str


@app.post("/parse-gh/")
def parse_gh(link: GHLink):
    try:
        folder_name = download_github_repo(link.gh_link)
        return {"folder_name": folder_name}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/get-summary/")
def parse_gh(link: GHLink):
    try:
        info = get_repo_info(link.gh_link)
        return json.loads(info)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/get-description")
def parse_gh(link: GHLink):
    try:
        info = get_suggestion(link.gh_link)
        return json.loads(info.text)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
