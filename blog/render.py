import markdown

from markdown.extensions.toc import TocExtension


def read_file_content(filename: str) -> str:
    with open(filename) as f:
        return f.read()


def write_file_content(filename: str, data: str) -> None:
    with open(filename, mode='w') as f:
        f.write(data)


def to_html(filename: str) -> str:
    text = read_file_content(filename)
    return markdown.markdown(text, extensions=["fenced_code", "footnotes",
                                               TocExtension(anchorlink=True)])
