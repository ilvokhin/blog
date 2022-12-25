TEMPLATES := $(shell find templates -name '*.html' 2> /dev/null)
SHARE := $(shell find share -name '*' 2> /dev/null)
POSTS := $(shell find posts -name '*' 2> /dev/null)
CODE := $(shell find blog -name '*.py' 2> /dev/null)

.PHONY: clean httpserver

remote: $(TEMPLATES) $(SHARE) $(POSTS)
	python3 blog/blog.py

httpserver: remote
	python3 -m http.server --directory remote

clean:
	rm -rf remote
