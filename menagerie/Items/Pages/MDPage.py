import re
from pathlib import Path

from markdown import Markdown, Extension
from markdown.treeprocessors import Treeprocessor
from markdown.extensions.admonition import AdmonitionProcessor

from menagerie.Items.Pages.AbstractPage import AbstractPage

__all__ = ('MDPage',)

ADDITIONAL_CLASSES: dict[str, str] = {
    'img': "img-fluid rounded mx-auto d-flex",
    'table': "table table-striped"
}


class MTreeProcessor(Treeprocessor):

    def __init__(self, page):
        super().__init__()
        self.page = page

    def run(self, node):
        for child in node:
            self.page.process_node(child)
        return node


class MenagerieAdmonitions(AdmonitionProcessor):

    CLASSNAME = "alert"
    CLASSNAME_TITLE = "h4"


class MenagerieMarkdownExtension(Extension):

    def __init__(self, page, **kwargs):
        self.page = page
        super().__init__(**kwargs)

    def extendMarkdown(self, md: Markdown) -> None:
        md.registerExtension(self)
        self.tree = MTreeProcessor(self.page)
        self.tree.md = md
        self.tree.config = self.getConfigs()
        md.treeprocessors.add('menagerie_tree', self.tree, '_end')
        md.parser.blockprocessors.register(MenagerieAdmonitions(md.parser), 'm-admonition', 105)



class MDPage(AbstractPage):
    extensions = ('md', 'markdown')

    md: Markdown

    def process_node(self, node) -> None:
        if node.tag in ADDITIONAL_CLASSES.keys():
            node.set('class', ADDITIONAL_CLASSES[node.tag])
        if node.tag == 'img':
            possible_match = re.match(r"{{ ?[\"'](.*?)['\"]\|static.*?}}", node.get('src'))
            if possible_match:
                image_path = possible_match.group(1)
                size = self.manager.gen.shared_info['image_sizes'].get(str(Path(image_path).as_posix()), (100, 100))
                node.set('width', str(size[0]))
                node.set('height', str(size[1]))
        for child in node:
            self.process_node(child)

    def __init__(self, manager, path: Path):
        super(MDPage, self).__init__(manager, path)
        md_settings = {
            'extensions': ['extra', 'toc', 'meta', MenagerieMarkdownExtension(self)],
            'output-format': 'html5'
        }
        self.md = Markdown(**md_settings)

    def load_metadata(self) -> None:
        self.md.convert(self.get_content()).replace('&quot;', '"')
        self.meta.update({k: None if v is None else v[0] for k, v in self.md.Meta.items()})
        self.meta['table_of_contents'] = self.md.toc_tokens

    def inner_render(self, content: str) -> str:
        converted = self.md.convert(self.get_content()).replace('&quot;', '"')
        return self.manager.env.from_string(converted).render(page=self, **self.manager.context)
