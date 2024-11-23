import requests
from bs4 import BeautifulSoup as bs


def lu_parse(url):

    resp = requests.get(url)

    assert resp.status_code == 200

    html = resp.text
    soup = bs(html, features="html.parser")

    title = soup.find("h1").get_text()

    start_span, end_span, *_ = soup.find_all("span", attrs={"class": "date"})

    start = start_span.get_text()[:4]
    end = end_span.get_text()[:4]

    return {
        "name": title,
        "year": int(start),
        "end": int(end),
        "town": "Lund",
        "url": url,
    }
