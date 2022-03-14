from pathlib import Path

from markdown import Markdown

from Items.Pages.AbstractPage import AbstractPage

__all__ = ('MDPage',)

MARKDOWN_SETTINGS = {
    'extensions': ['extra', 'toc', 'meta'],
    'output-format': 'html5'
}


class MDPage(AbstractPage):

    extensions = ('md', 'markdown')

    md: Markdown

    def __init__(self, manager, path: Path):
        super().__init__(manager, path)
        self.md = Markdown(**MARKDOWN_SETTINGS)
        self.rendered_markdown = None

    def load_metadata(self) -> None:
        self.rendered_markdown = self.md.convert(self.content)
        # noinspection PyUnresolvedReferences
        self.meta.update({k: None if v is None else v[0] for k, v in self.md.Meta.items()})

    def inner_render(self, content: str) -> str:
        return self.manager.env.from_string(self.rendered_markdown).render(page=self, **self.manager.context)
