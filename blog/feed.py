import os
from typing import List

from jinja2 import Template

import render
from post import Post


class Feed(object):
    template: Template
    posts: List[Post]

    def __init__(self, template: Template, posts: List[Post]) -> None:
        self.template = template
        self.posts = Feed._remove_drafts(posts)

    @staticmethod
    def _remove_drafts(posts: List[Post]) -> List[Post]:
        return list(filter(lambda x: x.metadata.status != "draft", posts))

    def generate(self, basedir: str) -> None:
        index = os.path.join(basedir, "index.html")
        rendered = self.template.render(posts=self.posts)
        render.write_file_content(index, rendered)
