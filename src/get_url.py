import re
import subprocess
from random import shuffle
from time import sleep

import requests
from bs4 import BeautifulSoup as bs
from tqdm import tqdm

from get_gu import gu_parse
from get_lu import lu_parse
from get_mau import mau_parse
from get_oru import oru_parse
from get_su import su_parse
from get_umu import umu_parse
from get_uu import uu_parse
from paths import projects, url_file
from project_to_yaml import write_project


def load_urls():
    with open(projects, "r", encoding="utf8") as f:
        proj_txt = f.read()
    used_urls = set(re.findall("https://\S+\n", proj_txt))

    with open(url_file, "r", encoding="utf8") as f:
        lines = list(
            set(
                filter(lambda line: line != "" and line not in used_urls, f.readlines())
            )
        )

    shuffle(lines)

    with tqdm(total=len(lines)) as bar:
        while len(lines) > 0:
            line = lines.pop()
            yield line.strip()

            with open(url_file, "w", encoding="utf8") as f:
                f.writelines(sorted(lines))
            bar.update(1)
            try:
                first = subprocess.run(["git", "commit", "-am", f'"Format"'])
            finally:
                second = subprocess.check_output(
                    ["git", "commit", "-am", f'"Add {line}"']
                )
                assert b"failed" not in second


def archive(url):
    saved_response = requests.get("https://web.archive.org/save/" + url)
    saved_url = saved_response.url
    while not saved_url.startswith("https://web.archive.org/web/"):
        sleep(10)
        saved_response = requests.get("https://web.archive.org/save/" + url)
        saved_url = saved_response.url

    assert saved_url.endswith(url)


if __name__ == "__main__":
    assert b"On branch main" not in subprocess.check_output(["git", "status"])
    for i, url in enumerate(load_urls()):
        if i > 0:
            sleep(10)

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
        elif url.startswith("https://www.su.se/forskning/forskningsprojekt"):
            project_data = su_parse(url)
        else:
            raise ValueError(url)

        write_project(project_data)
        archive(url)
