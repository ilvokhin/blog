TEMPLATES := $(shell find templates -name '*.html' 2> /dev/null)
SHARE := $(shell find share -name '*' 2> /dev/null)
POSTS := $(shell find posts -name '*' 2> /dev/null)
CODE := $(shell find blog -name '*.py' 2> /dev/null)

.PHONY: clean server

remote: $(TEMPLATES) $(SHARE) $(POSTS)
	python3 blog/blog.py

server: remote
	python3 -m http.server --directory remote

deploy: remote
	rsync -avzP --delete remote/ blog.ilvokhin.com:/var/www/blog.ilvokhin.com/
	ssh blog.ilvokhin.com -- chown -R d:http /var/www/blog.ilvokhin.com/

clean:
	rm -rf remote
