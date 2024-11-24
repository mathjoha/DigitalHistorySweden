import re
import webbrowser

import requests
from bs4 import BeautifulSoup as bs


def su_parse(url):

    resp = requests.get(url)

    assert resp.status_code == 200

    html = resp.text
    soup = bs(html, features="html.parser")

    h1 = soup.find("h1")

    h1.find("span").clear()

    title = (
        h1.get_text()
        .replace("\r\n", "")
        .replace(r"\\\n    \\", "")
        .strip()
        .replace("\n", "")
    )

    overview_div = soup.find(
        lambda tag: tag.name == "div" and tag.text.strip().startswith("Projektperiod")
    )

    start, end, *_ = re.findall(r"\d{4}", overview_div.get_text())

    return {
        "name": title.strip(),
        "year": int(start),
        "end": int(end),
        "town": "Stockholm",
        "url": url,
    }
