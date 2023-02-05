import os
import shutil
import datetime
import functools
from typing import Dict

from jinja2 import Template

import render


class Metadata(object):
    __slots__ = ("title", "date", "status")
    title: str
    date: str
    status: str

    def __init__(self, title: str, date: str, status: str) -> None:
        self.title = title
        self.date = date
        self.status = status


class Post(object):
    template: Template
    directory: str
    name: str

    def __init__(self, template: Template, directory: str) -> None:
        self.template = template
        self.directory = directory
        self.name = os.path.basename(directory)

    @staticmethod
    def _load_raw_metadata(filename: str) -> Dict[str, str]:
        data = {}

        with open(filename) as f:
            for line in f:
                k, v = line.strip().split(": ")
                data[k] = v

        return data

    @functools.cached_property
    def metadata(self) -> Metadata:
        raw = Post._load_raw_metadata(os.path.join(self.directory,
                                                   "metadata.txt"))

        title = raw["Title"]
        date = raw.get("Date", datetime.date.today().strftime("%Y-%m-%d"))
        status = raw.get("Status", "draft")

        return Metadata(title, date, status)

    def generate(self, basedir: str) -> None:
        postdir = os.path.basename(self.directory)
        workdir = os.path.join(basedir, postdir)
        os.makedirs(workdir)

        md = None
        for filename in os.listdir(self.directory):
            source = os.path.join(self.directory, filename)
            destination = os.path.join(workdir, filename)

            shutil.copy(source, destination)

            if filename.endswith(".md"):
                md = source

        assert md, f"There is no markdown file in `{self.directory}`"

        content = render.to_html(md)
        rendered = self.template.render(title=self.metadata.title,
                                        date=self.metadata.date,
                                        status=self.metadata.status,
                                        content=content)
        render.write_file_content(os.path.join(workdir, "index.html"),
                                  rendered)
