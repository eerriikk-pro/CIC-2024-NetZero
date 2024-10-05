import requests
import re
import zipfile
import io

# url = "https://api.github.com/repos/eerriikk-pro/nwHacks2024/zipball"
# response = requests.request("GET", url)

# print(response.text)
# filename = "test"

# if response.status_code == 200:
#     filename = "nwHacks2024.zip"
#     with open(filename, "wb") as file:
#         file.write(response.content)
#     print(f"Data saved to {filename}")
# else:
#     print(f"Failed to retrieve data: {response.status_code} {response.reason}")


def download_github_repo(repo_url):
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

        # unzip the file on 200
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(f"{repo}")
        print(f"Data extracted to {repo}/")
    else:
        print(f"Failed to retrieve data: {response.status_code} {response.reason}")


# testing
repo_url = "https://github.com/eerriikk-pro/nwHacks2024"
download_github_repo(repo_url)