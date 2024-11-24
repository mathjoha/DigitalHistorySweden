from collections import Counter
from pathlib import Path

try:
    import yaml
except ModuleNotFoundError:
    import subprocess
    import sys

    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyyaml"])

    import yaml


project_yaml_path = Path(__file__).parent / "projects.yaml"


def sort_order(project: dict):
    """Sort project yaml file for consistency.

    year(started): descending
    (year)end: descending [adds a placeholder if no end is specified]
    project name: alphabetical
    project town: alphabetical

    """
    project["end"] = project["end"] if "end" in project.keys() else 9999

    if project["end"] < project["year"]:
        raise ValueError("Project {project} ends before it starts")

    return (
        -project["year"],
        -project["end"],
        project["name"].strip(),
        project["town"].strip(),
    )


if __name__ == "__main__":
    with open(project_yaml_path, "r", encoding="utf8") as f:
        raw_yaml = f.read()

    projects_dicts = yaml.safe_load(raw_yaml)

    names_count = Counter((proj["name"].strip() for proj in projects_dicts))

    duplicate_names = [
        (name, count) for name, count in names_count.items() if count > 1
    ]

    if len(duplicate_names) > 0:
        raise ValueError(f"Duplicate project name found: {duplicate_names}")

    sorted_projects = sorted(projects_dicts, key=sort_order)

    sorted_yaml = yaml.safe_dump(sorted_projects)

    if sorted_yaml != raw_yaml:
        with open(project_yaml_path, "w", encoding="utf8") as f:
            f.write(sorted_yaml)
