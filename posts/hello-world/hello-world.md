Occasionally, I find something interesting worth sharing. But there is no ideal
place where I can write it down, so I decided to create such place.

There are a lot of blog platforms around. But I usually don't quite like some
little details about them. I wanted something self-hosted, fast (in case I'll
write something that will be on the Hacker News front page), simple and easy to
maintain.

Once, I found the [Telegra.ph][1] publishing tool, which is pretty nice, but
isn't self-hosted. So, I figured, maybe I can build something similar myself.

## Requirements

Here is the list of requirements I had in mind, when was thinking about what I
want to see at the end. I wouldn't even call them requirements, to be honest,
more like guiding principles.

### Own Everything

The biggest thing I don't like about existing blog and publishing tools is I
don't own and don't have a complete control for everything, starting from the
domain name and ending with how URLs for posts will look like. This wish
motivated by the fact I want to have stable URLs, that will not break in the
future.

Moreover, I want to control the platform itself. This way it will last as long
as I have a desire to support it and won't be shutdown, because of big company
priorities shift. And there will be no unexpected policies additions that may
cause content to be removed or changed. Not that I'm going to post anything
controversial. But the concept of controversial rather blurry nowadays.

### Speed

A few things compare with static content serving in terms of speed. Therefore,
I better serve static content then. It shouldn't be the problem, because I am
going to share mostly texts anyway. Generate once, share many times. Seems like
a good strategy for me.

### Format

I was thinking about a format for some time. I like LaTeX. A lot. Also, this
would save me completely from the web design (I don't know how to do a CSS
properly for example).

But I am going to write primarily about computers with some code and to my
shame for all this years I still didn't figure out a way how to make code look
at least bearable. Besides, I am not sure it is convenient enough to read
something from the PDF. Of course, if you are going to read a research paper
(this process will probably take a couple of weeks), then maybe, but not for
some random text you just found on the Internet and not even sure you are
interested in. I heard HTML is a right format for the Internet stuff, so HTML
it is. Probably, one day I'll figure out a way to generate good looking PDFs
and HTML pages at the same time, but not today.

### Maintenance

So far probably every mature static site generator would be a good fit for me.
I started playing with [Hugo][2]. But then I found this [Twitter][3] thread from
Dan Luu, which decreased my enthusiasm for Hugo, because I hate fixing stuff,
especially one I didn't break myself. Likely, situation already changed, but
there is no guarantee there will be no other breaking changes in the future.

## Design

After I take a look on the list of the requirements, I decided to reinvent the
wheel and write my own static site generator, tailored exactly for my needs.

I want to publish some text content and I am going to need the following to make
it usable.

1. Publishing interface.
2. List of already published content.
3. Pages with a content itself.

Separate web page for content publishing sounds cool, but looks like unnecessary
thing to have. I can use the usual text editor of my choice to write text,
manually regenerate content and push update to the server. I am too lazy to
write HTML by hands, so Markdown seems like a reasonable tool for this job.

The picture is slowly coming together. I am going to have a bunch of Markdown
files with content, then HTML pages will be generated out of this files and as
a last step, everything will be pushed to serving server. Code for content
generation and raw content itself can be stored together in version control
system.

One more thing to think about is a directory structure. I don't want to
have only text in the post. Sometimes there will be pictures (I hope). So, I
need a place to store them. Naming is a hard thing to do and over time I'll
for sure will have a few files with the short name like `algorithm.png`, but
with a different content. To avoid collisions and to save myself from future
pain, it is better to store pictures for each post separately.

```
% tree posts
posts
├── hashtables
│   ├── hashtables.md
│   ├── metadata.txt
│   └── picture.png
└── hello-world
    ├── hello-world.md
    ├── metadata.txt
    └── picture.png
```

Furthermore, posts might have some metadata associated with them. For example,
title, publish date, author etc. At the beginning, I was thinking to combine
content and metadata together in one file, but all solutions I came up with were
awkward (have necessary info on top of the md file as a comment or cut it out
manually before pass it to Markdown parser), therefore I decided to abandon
this idea. For that reason directory per post comes in handy with the idea of
metadata and content separation.

Separation idea has some advantages.

* Simpler implementation. I don't need to wrangle with text replacement.
* No need to open and parse heavy file with content to extract required fields.

One of the disadvantages is necessity of two files editing for post creation.
Over time, it will become clearer how much inconvenience this will bring.


## Implementation

The plan was to implement the following pipeline, which (I believe) is a quite
common for static sites at the moment.

```
Localhost:
.---------------.        .---------------.        .---------------.
|               |  (1)   |               |  (2)   |               |
|  Raw Content  | -----> |   Generator   | -----> |  HTML Content |
|  (Markdown)   |        |   (Python)    |        |               |
.---------------.        .---------------.        .---------------.
\                                       /                |
 \                 Git                 /                 |
  -------------------------------------                  | 
                                                         |
                                                         |
Remote server:                                           |
.---------------.                                        |  (3)
|               |                                        | Rsync
|     Nginx     | <--------------------------------------.
|               |
.---------------.
        ^
        |
        |
        | (4)
        |
        |

       User
```

At this picture steps (1), (2), (3) are preparation steps to write, generate
and sync content with a remote server and step (4) is a step to serve the
site content to the happy user.

Almost all building blocks on this diagram are fairly common and well know
tools. The only one custom component is a Generator (from Markdown to HTML)
itself. It took less than 200 lines to implement desired logic with [Jinja][4]
as a template engine and [Markdown][5] library for markup support.

```
% wc -l blog/*py
       0 blog/__init__.py
      59 blog/blog.py
      14 blog/feed.py
      68 blog/post.py
      16 blog/render.py
     157 total
```

Only one thing made me worry - CSS and design overall. I want to have something
simple, with a focus on the content itself. Luckily, I found Herman Martinus
[Bear Blog][6]. It looks quite similar to what I want to have at the beginning
(see Telegra.ph text example [here][7]). I used Bear Blog Cascading Style
Sheets as a starting point, made couple of "improvements" here and there,
removed things I don't understand and voilà.

The last thing I added was a feature to fire up a web server on localhost with
a complete copy of the website to see how everything will look. This was a final
touch, to simplify and ease the writing process for myself.

If you are interested in details, you can find the source code on [Github][8].

## Future Work

One thing I want to have and really missing comparing with real blog platforms
is some kind of statistics, at least the basic one: how often some page was
viewed, how much unique visitors I had and where they are coming from.

I believe some (if not all) of this information can be extracted from the Nginx
access logs, but I didn't come up with a good solution for this problem yet.


[1]: https://telegra.ph
[2]: https://gohugo.io
[3]: https://twitter.com/danluu/status/1434282814510403584
[4]: https://jinja.palletsprojects.com
[5]: https://python-markdown.github.io
[6]: https://bearblog.dev
[7]: https://telegra.ph/Example-01-08-2
[8]: https://github.com/ilvokhin/blog
