import json

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ec2_gh.main import download_github_repo, get_repo_info

# Instantiate the class
app = FastAPI()


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
