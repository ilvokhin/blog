TEMPLATES := $(shell find templates -name '*.html' 2> /dev/null)
SHARE := $(shell find share -name '*' 2> /dev/null)
POSTS := $(shell find posts -name '*' 2> /dev/null)
CODE := $(shell find blog -name '*.py' 2> /dev/null)

.PHONY: typecheck format server deploy clean

remote: $(TEMPLATES) $(SHARE) $(POSTS) $(CODE) typecheck
	python3 blog/blog.py

typecheck: $(CODE)
	mypy --strict blog

format: $(CODE)
	pycodestyle $(CODE)

server: remote
	python3 -m http.server --directory remote

deploy: remote
	rsync \
        --recursive \
        --compress \
        --links \
        --progress \
        --delete \
        remote/ \
        blog.ilvokhin.com:/srv/http/blog.ilvokhin.com

clean:
	rm -rf remote
