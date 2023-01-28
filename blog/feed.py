import os

import render


class Feed(object):
    def __init__(self, template, posts):
        self.template = template
        self.posts = Feed._remove_drafts(posts)

    @staticmethod
    def _remove_drafts(posts):
        return list(filter(lambda x: x.metadata.status != "draft", posts))

    def generate(self, basedir):
        index = os.path.join(basedir, "index.html")
        rendered = self.template.render(posts=self.posts)
        render.write_file_content(index, rendered)
