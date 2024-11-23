from bs4 import BeautifulSoup as bs

from get_lu import lu_parse
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

        write_project(project_data)
