import re
import webbrowser

import requests
from bs4 import BeautifulSoup as bs

translator = {"Riksantikvarieämbetet": "Stockholm"}


def raa_parse(url):

    resp = requests.get(url)

    assert resp.status_code == 200

    html = resp.text
    soup = bs(html, features="html.parser")

    title = (
        soup.find(lambda tag: tag.name == "tr" and tag.text.startswith("Titel"))
        .find(lambda tag: tag.name == "td" and not tag.text.startswith("Titel"))
        .get_text()
    )

    overview = soup.find("td", attrs={"class": "frmTable"}).get_text()

    years = [int(_) for _ in re.findall(r"\d{4}", overview)]

    town = (
        soup.find(
            lambda tag: tag.name == "tr" and tag.text.startswith("Medelsförvaltare")
        )
        .find(
            lambda tag: tag.name == "td" and not tag.text.startswith("Medelsförvaltare")
        )
        .get_text()
    )

    if town in translator:
        town = translator[town]

    return {
        "name": title.strip(),
        "year": min(years),
        "end": max(years),
        "town": town,
        "url": url,
    }
