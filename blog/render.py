import markdown


def read_file_content(filename):
    with open(filename) as f:
        return f.read()


def write_file_content(filename, data):
    with open(filename, mode='w') as f:
        f.write(data)


def to_html(filename):
    text = read_file_content(filename)
    return markdown.markdown(text, extensions=["fenced_code", "footnotes"])
