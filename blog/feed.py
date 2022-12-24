import os

import render


class Feed(object):
    def __init__(self, template, posts):
        self.template = template
        self.posts = posts

    def generate(self, basedir):
        index = os.path.join(basedir, "index.html")
        rendered = self.template.render(posts=self.posts)
        render.write_file_content(index, rendered)
