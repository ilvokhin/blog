#! /usr/bin/env python3
# -*- coding: utf-8 -*

import os
import shutil
import argparse
from typing import List

from jinja2 import Template, Environment, FileSystemLoader, select_autoescape

from post import Post
from feed import Feed


def recreate_workdir(basedir: str) -> None:
    if os.path.exists(basedir):
        shutil.rmtree(basedir)
    os.makedirs(basedir)


def find_posts(template: Template, basedir: str) -> List[Post]:
    posts = []
    for subdir in os.listdir(basedir):
        posts.append(Post(template, os.path.join(basedir, subdir)))
    return posts


def copy_share(workdir: str) -> None:
    for filename in os.listdir("share"):
        source = os.path.join("share", filename)
        destination = os.path.join(workdir, filename)

        shutil.copy(source, destination)


def generate_blog() -> None:
    env = Environment(loader=FileSystemLoader(searchpath="templates"),
                      autoescape=select_autoescape())

    posts = find_posts(env.get_template("post.html"), "posts")
    posts = sorted(posts, key=lambda x: x.metadata.date, reverse=True)

    workdir = "remote"
    recreate_workdir(workdir)

    for post in posts:
        post.generate(workdir)

    feed = Feed(env.get_template("feed.html"), posts)
    feed.generate(workdir)

    copy_share(workdir)


def main() -> None:
    generate_blog()


if __name__ == "__main__":
    main()
