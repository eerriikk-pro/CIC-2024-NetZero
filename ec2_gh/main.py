import requests

url = "https://api.github.com/repos/eerriikk-pro/nwHacks2024/zipball"
response = requests.request("GET", url)

print(response.text)
filename = "test"

if response.status_code == 200:
    filename = "nwHacks2024.zip"
    with open(filename, "wb") as file:
        file.write(response.content)
    print(f"Data saved to {filename}")
else:
    print(f"Failed to retrieve data: {response.status_code} {response.reason}")
