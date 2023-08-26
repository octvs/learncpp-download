import os
from pathlib import Path

import requests
from readability import Document
from tqdm import tqdm

import scraper

HEADER = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>%s</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <style type="text/css">
        body {
            font-size: 25px;
            font-family: "Noto",sans-serif;
            margin: auto;
            max-width: 55vw;
            min-width: 650px;
            line-height: 1.4;
            color: #ebdbb2;
            background-color: #202020;
        }
        h1, h2, h3 {
            line-height: 1.2;
        }
        a{
            color: #83a598;
        }
    </style>
</head>
"""

for url in tqdm(scraper.get_urls()):
    html = requests.get(url)

    doc = Document(html.text)
    title = doc.title()
    lesson_idx = title.split(" ")[0]
    content = doc.summary().replace("<html>", HEADER % title)

    download_dir = Path(os.environ["XDG_DOWNLOAD_DIR"]).joinpath("learncpp")
    download_dir.mkdir(exist_ok=True)

    with open(download_dir.joinpath(lesson_idx + ".html"), "w") as target:
        target.write(content.lstrip())
