import os

import requests


def download_pdf(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Downloaded: {filename}")
    else:
        print("Failed to download file:", response.status_code)


# Create a folder to save the PDFs
folder_name = "sus_files"
os.makedirs(folder_name, exist_ok=True)

# List of PDF URLs
pdf_urls = [
    "https://arxiv.org/pdf/2311.16863",
    "https://arxiv.org/pdf/2310.03003",
    "https://arxiv.org/pdf/2104.10350",
    "https://dl.acm.org/doi/pdf/10.1145/3610954",
]

if __name__ == "__main__":
    # Download each PDF into the folder
    for url in pdf_urls:
        filename = os.path.join(
            folder_name, url.split("/")[-1] + ".pdf"
        )  # Construct the file path
        download_pdf(url, filename)
