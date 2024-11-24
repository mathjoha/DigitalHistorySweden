import requests
from bs4 import BeautifulSoup as bs

from get_gu import gu_parse
from get_lu import lu_parse
from get_mau import mau_parse
from get_oru import oru_parse
from get_umu import umu_parse
from get_uu import uu_parse
from paths import url_file
from project_to_yaml import write_project


def load_urls():
    with open(url_file, "r", encoding="utf8") as f:
        for line in f.readlines():
            yield line.strip()


if __name__ == "__main__":
    for url in load_urls():
        if "portal.research.lu.se" in url:
            project_data = lu_parse(url)
        elif url.startswith("https://www.umu.se/en/research/projects/"):
            project_data = umu_parse(url)
        elif url.startswith("https://www.uu.se/en/research/research-projects/project"):
            project_data = uu_parse(url)
        elif url.startswith("https://www.gu.se/en/research"):
            project_data = gu_parse(url)
        elif url.startswith(
            "https://www.oru.se/english/research/research-projects/rp/?rdb="
        ):
            project_data = oru_parse(url)
        elif url.startswith("https://mau.se/en/research/projects/"):
            project_data = mau_parse(url)

        write_project(project_data)
        saved_response = requests.get("https://web.archive.org/save/" + url)
        saved_url = saved_response.url
        assert saved_url.startswith("https://web.archive.org/web/")
        assert saved_url.endswith(url)

        break
