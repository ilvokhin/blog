import os
import datetime
from typing import List

from jinja2 import Template

import render
from post import Post, remove_drafts


class Feed(object):
    template: Template
    posts: List[Post]

    def __init__(self, template: Template, posts: List[Post]) -> None:
        self.template = template
        self.posts = remove_drafts(posts)

    def generate(self, basedir: str) -> None:
        index = os.path.join(basedir, "index.html")
        rendered = self.template.render(posts=self.posts)
        render.write_file_content(index, rendered)
