# Simple static blog (generator code and content)

## Install

```
$ python3 -m venv .env
$ source .env/bin/activate
$ pip3 install -r requirements.txt
```

## Make a post

```
$ mkdir posts/hello-world
$ echo 'Title: Hello, World!' > posts/hello-world/metadata.txt
$ echo 'Date: 2022-12-23' >> posts/hello-world/metadata.txt
$ echo 'Hello, world!' > posts/hello-world/hello-world.txt
$ make deploy
```

## Demo

Visit [blog.ilvokhin.com][1] to see the working demo.


[1]: https://blog.ilvokhin.com
