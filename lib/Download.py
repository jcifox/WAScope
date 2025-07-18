import requests


# download source
def download_source(url, output_path, chunk_size=512):
    response = requests.get(url=url, stream=True)
    with open(output_path, mode='wb') as f:
        for chunk in response.iter_content(chunk_size):
            f.write(chunk)
