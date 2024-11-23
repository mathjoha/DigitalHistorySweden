import re

import yaml

from paths import projects


def write_project(project_data):
    yaml_lines = re.sub(
        r"\n",
        "\n  ",
        re.sub(
            r"^",
            "- ",
            yaml.safe_dump(project_data),
        ),
    )

    with open(projects, "a", encoding="utf8") as project_yaml:
        project_yaml.write(yaml_lines)


if __name__ == "__main__":
    write_project(
        {"name": "Title", "year": "START", "end": "END", "town": "Lund", "url": "URL"}
    )
