import re
from pathlib import Path

from markdown import Markdown, Extension
from markdown.treeprocessors import Treeprocessor

from menagerie.Items.Managers.StaticManager import StaticManager
from menagerie.Items.Pages.AbstractPage import AbstractPage
from menagerie.Items.Static.StaticImage import StaticImage
from menagerie.Settings import Settings

__all__ = ('MDPage',)

MARKDOWN_SETTINGS = {
    'extensions': ['extra', 'toc', 'meta', MenagerieMarkdownExtension()],
    'output-format': 'html5'
}

ADDITIONAL_CLASSES: dict[str, str] = {
    'img': "img-fluid rounded mx-auto d-flex",
    'table': "table-striped"
}

def process_node(node) -> None:
    if node.tag in ADDITIONAL_CLASSES.keys():
        node.set('class', ADDITIONAL_CLASSES[node.tag])
    if node.tag == 'img':
        possible_match = re.match(r"{{ ?\"(.*?)\"\|static.*?}}", node.get('src'))
        if possible_match:
            image_path = StaticManager.get_static(possible_match.group()[0])
            size = StaticImage.get_size(str(Path(image_path).relative_to(Settings.out_dir)))
            node.set('width', size[0])
            node.set('height', size[1])
    for child in node:
        process_node(node)


class MTreeProcessor(Treeprocessor):

    def run(self, node):
        for child in node:
            process_node(node)
        return node


class MenagerieMarkdownExtension(Extension):

    def extendMarkdown(self, md: Markdown) -> None:
        md.register_extension(self)
        self.tree = MTreeProcessor()
        self.tree.md = md
        self.tree.config = self.getConfigs()
        md.treeprocessors.add('menagerie_tree', self.tree, '_end')



class MDPage(AbstractPage):

    extensions = ('md', 'markdown')

    md: Markdown

    def __init__(self, manager, path: Path):
        super().__init__(manager, path)
        self.md = Markdown(**MARKDOWN_SETTINGS)
        self.rendered_markdown = None

    def load_metadata(self) -> None:
        self.rendered_markdown = self.md.convert(self.get_content())
        # noinspection PyUnresolvedReferences
        self.meta.update({k: None if v is None else v[0] for k, v in self.md.Meta.items()})

    def inner_render(self, content: str) -> str:
        return self.manager.env.from_string(self.rendered_markdown).render(page=self, **self.manager.context)
