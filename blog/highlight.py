import os
from typing import cast, Callable

from pygments.formatters import HtmlFormatter


def get_style_defs() -> str:
    # Workaround to avoid mypy to complain about untyped
    # get_style_defs() call.
    formatter = HtmlFormatter(style="bw")
    selector = ".highlight"
    f = cast(Callable[[str], str], formatter.get_style_defs)
    return f(selector)


class Highlight(object):
    @staticmethod
    def generate(basedir: str) -> None:
        highligh = os.path.join(basedir, "highlight.css")

        with open(highligh, mode='w') as f:
            style = get_style_defs()
            f.write(style)
