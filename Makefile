TEMPLATES := $(shell find templates -name '*.html' 2> /dev/null)
SHARE := $(shell find share -name '*' 2> /dev/null)
POSTS := $(shell find posts -name '*' 2> /dev/null)
CODE := $(shell find blog -name '*.py' 2> /dev/null)

.PHONY: clean

remote: $(TEMPLATES) $(SHARE) $(POSTS)
	python3 blog/blog.py

clean:
	rm -rf remote
