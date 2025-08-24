import os
import shutil
import datetime
import functools
from typing import Dict, List

from jinja2 import Template

from dataclasses import dataclass

import render


@dataclass
class Metadata(object):
    title: str
    author: str
    date: datetime.datetime
    updated: datetime.datetime
    status: str


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
        author = raw["Author"]
        date = raw["Date"]
        updated = raw.get("Updated", date)
        status = raw.get("Status", "draft")

        return Metadata(
                title,
                author,
                datetime.datetime.fromisoformat(date),
                datetime.datetime.fromisoformat(updated),
                status
        )

    @functools.cached_property
    def content(self) -> str:
        md = None
        for filename in os.listdir(self.directory):
            if filename.endswith(".md"):
                return render.to_html(os.path.join(self.directory, filename))
        assert False, f"There is no markdown file in `{self.directory}`"

    def generate(self, basedir: str) -> None:
        postdir = os.path.basename(self.directory)
        workdir = os.path.join(basedir, postdir)
        os.makedirs(workdir)

        for filename in os.listdir(self.directory):
            source = os.path.join(self.directory, filename)
            destination = os.path.join(workdir, filename)
            shutil.copy(source, destination)

        rendered = self.template.render(title=self.metadata.title,
                                        author=self.metadata.author,
                                        date=self.metadata.date,
                                        updated=self.metadata.updated,
                                        status=self.metadata.status,
                                        content=self.content)
        render.write_file_content(os.path.join(workdir, "index.html"),
                                  rendered)


def remove_drafts(posts: List[Post]) -> List[Post]:
    return list(filter(lambda x: x.metadata.status != "draft", posts))
