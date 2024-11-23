import re
import webbrowser

import requests
from bs4 import BeautifulSoup as bs


def uu_parse(url):

    resp = requests.get(url)

    assert resp.status_code == 200

    html = resp.text
    soup = bs(html, features="html.parser")

    title = (
        soup.find("h1")
        .get_text()
        .replace("\r\n", "")
        .replace(r"\\\n    \\", "")
        .strip()
        .replace("\n", "")
    )

    overview_div = soup.find("div", attrs={"class": "programmeOverview"}).get_text()

    start, end, *_ = re.findall(r"\d{4}", overview_div)

    return {
        "name": title.strip(),
        "year": int(start),
        "end": int(end),
        "town": "Umeå",
        "url": url,
    }
