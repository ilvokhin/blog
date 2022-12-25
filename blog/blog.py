#! /usr/bin/env python3
# -*- coding: utf-8 -*

import os
import shutil

from jinja2 import Environment, FileSystemLoader, select_autoescape

from post import Post
from feed import Feed


def recreate_workdir(basedir):
    if os.path.exists(basedir):
        shutil.rmtree(basedir)
    os.makedirs(basedir)


def find_posts(template, basedir):
    posts = []
    for subdir in os.listdir(basedir):
        posts.append(Post(template, os.path.join(basedir, subdir)))
    return posts

def copy_share(workdir):
    for filename in os.listdir("share"):
        source = os.path.join("share", filename)
        destination = os.path.join(workdir, filename)

        shutil.copy(source, destination)


def generate_blog(include_drafts=False):
    env = Environment(loader=FileSystemLoader(searchpath="templates"),
                      autoescape=select_autoescape())

    posts = find_posts(env.get_template("post.html"),
                       os.path.join("posts", "public"))

    if include_drafts:
        drafts = find_posts(env.get_template("post.html"),
                            os.path.join("posts", "drafts"))
        posts.extend(drafts)

    workdir = "remote"
    recreate_workdir(workdir)

    for post in posts:
        post.generate(workdir)

    feed = Feed(env.get_template("feed.html"), posts)
    feed.generate(workdir)

    copy_share(workdir)


def main():
    generate_blog(include_drafts=True)


if __name__ == "__main__":
    main()
