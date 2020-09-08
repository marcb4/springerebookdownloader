import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
from tqdm import tqdm

urllist = []

with open("urls.txt", "r") as handle:
    urllist = handle.readlines()
    urllist = [x.replace('\n', '') for x in urllist]

for url in urllist:
    response = urllib.request.urlopen(url)
    data = response.read()      # a `bytes` object
    text = data.decode('utf-8') # a `str`; this step can't be used if data is binary
    soup = BeautifulSoup(text, 'html.parser')

    pdf = soup.find("a", {"class": "test-bookpdf-link"})
    epub = soup.find("a", {"class": "test-bookepub-link"})
    name = soup.find("div",  {"data-test": "book-title"}).text.replace("\n", "").replace(" ", "_")
    parsed_uri = urlparse(url)
    base = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

    if pdf is not None:
        url = str(pdf['href'])
        filename = "{name}.pdf".format(name=name)
        print("{base}{url}".format(base=base, url=url[1:]))
        response = requests.get("{base}{url}".format(base=base, url=url[1:]), stream=True)

        with open(filename, "wb") as handle:
            for data in tqdm(response.iter_content()):
                handle.write(data)

    if epub is not None:
        url = str(epub['href'])
        filename = "{name}.epub".format(name=name)
        print("{base}{url}".format(base=base, url=url[1:]))
        response = requests.get("{base}{url}".format(base=base, url=url[1:]), stream=True)

        with open(filename, "wb") as handle:
            for data in tqdm(response.iter_content()):
                handle.write(data)

