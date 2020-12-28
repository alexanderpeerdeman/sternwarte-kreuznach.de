import yaml
import os
import pathlib
import logging
import json
from bs4 import BeautifulSoup

CONTENT_PATH = "content"


def index_pages():
    pages_index = []
    for dirpath, _, filenames in os.walk(CONTENT_PATH):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            page_index = process_file(filepath, filename)
            if page_index is None:
                continue
            pages_index.append(page_index)

    return pages_index


def process_file(abspath, filename):
    if str.endswith(filename, ".html"):
        return process_html_file(abspath, filename)
    elif str.endswith(filename, ".md"):
        return process_md_file(abspath, filename)
    return


def process_html_file(abspath: str, filename: str):
    with open(abspath, "r") as f:
        content = f.read()

    page_name = filename.removesuffix(".html")
    logging.info(page_name)
    href = abspath.removeprefix(CONTENT_PATH)
    logging.info(href)

    return {
        "title": page_name,
        "href": href,
        "content": BeautifulSoup(content, "html.parser").get_text().strip()
    }


def process_md_file(abspath: str, filename: str):
    with open(abspath, "r") as f:
        content = f.read()

    content = content.split("---")
    front_matter = yaml.safe_load(content[1].strip())
    href = abspath.removeprefix(CONTENT_PATH).removesuffix(".md")
    if filename == "index.md" or filename == "_index.md":
        href = abspath.removeprefix(
            CONTENT_PATH).removesuffix(filename)

    return {
        "title": front_matter["title"],
        "href": href,
        "content": BeautifulSoup(content[2], "html.parser").get_text().strip()
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Build pages index")

    pages_index_relpath = "static/js/lunr"
    pathlib.Path(pages_index_relpath).mkdir(parents=True, exist_ok=True)

    with open(os.path.join(pages_index_relpath, "pages_index.json"), "w") as outfile:
        json.dump(index_pages(), outfile, ensure_ascii=False)

    logging.info("Index built.")
