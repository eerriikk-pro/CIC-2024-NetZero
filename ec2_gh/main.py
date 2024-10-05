# Imports
############################################
import requests
import re
import zipfile
import io
import os
import json


# Constants
############################################
# bedrock api url
bedrock_api = "url here"

# Functions
############################################

# Downloads a gitHub repository as a zip file and extract it
def download_github_repo(repo_url) -> str:
    # extract owner and repo name from the URL using regex match
    match = re.match(r'https://github.com/([^/]+)/([^/]+)', repo_url)
    if not match:
        print("Invalid GitHub URL")
        return

    owner, repo = match.groups()
    api_url = f"https://api.github.com/repos/{owner}/{repo}/zipball"
    
    response = requests.get(api_url)

    if response.status_code == 200:
        filename = f"{repo}.zip"
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"Data saved to {filename}")

        # create a directory to unzip the file into
        extract_dir = os.path.join("extracted_repos", f"{repo}_extracted")
        os.makedirs(extract_dir, exist_ok=True)
        
        # unzip the file on 200
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(extract_dir)
        print(f"Data extracted to {extract_dir}/")

        return extract_dir
    else:
        print(f"Failed to retrieve data: {response.status_code} {response.reason}")

# Reads a file and returns its content as a string
def read_file_to_string(file_path: str) -> str:
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Reads all files in a directory and returns their content as a string. 
# Each files content is separated by a newline character and the file name is included as a comment
def read_repo_to_string(repo_path: str) -> str:
    repo_content = ""
    for root, _, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_content = read_file_to_string(file_path)
            if file_content:
                repo_content += f"# {file_path}\n{file_content}\n\n"
    return repo_content

# Takes in a string representing the project, and creates a prompt to ask
# aws bedrock to identify all gen ai functions in the project
def create_prompt(project_str: str) -> str:
    prompt = (
        "Can you identify all generative AI functions and tokens in the following project. Can you also provide the integer number of functions, and  tokens used. Can you also provide a breif description of what the project does:\n\n"
        f"{project_str}\n\n"
    )
    return prompt


# Sends a request to the bedrock api with the project string as the prompt
def get_ai_response(prompt: str) -> str:
    payload = json.dumps({
        "prompt": prompt
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", bedrock_api, headers=headers, data=payload)
    return response.text


def get_repo_info(repo_url: str) -> str:
    repo_path = download_github_repo(repo_url)
    repo_str = read_repo_to_string(repo_path)
    prompt = create_prompt(repo_str)
    response = get_ai_response(prompt)
    return response

    



# testing
############################################
repo_url = "https://github.com/eerriikk-pro/nwHacks2024"
response = get_repo_info(repo_url)
print(response)