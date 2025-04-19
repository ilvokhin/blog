import os
import datetime
import functools
from typing import List

from jinja2 import Template

import render
from post import Post, remove_drafts


class Atom(object):
    template: Template
    posts: List[Post]

    def __init__(self, template: Template, posts: List[Post]) -> None:
        self.template = template
        self.posts = remove_drafts(posts)

    @staticmethod
    def _now() -> datetime.datetime:
        now = datetime.datetime.now(datetime.timezone.utc)
        return now.replace(microsecond=0)

    @functools.cached_property
    def updated(self) -> datetime.datetime:
        if not self.posts:
            return self._now()
        return self.posts[0].metadata.updated

    def generate(self, basedir: str) -> None:
        atom = os.path.join(basedir, "atom.xml")
        rendered = self.template.render(updated=self.updated, posts=self.posts)
        render.write_file_content(atom, rendered)
