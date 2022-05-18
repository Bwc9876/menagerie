import re
from pathlib import Path

from markdown import Markdown, Extension
from markdown.extensions.attr_list import AttrListExtension, get_attrs
from markdown.treeprocessors import Treeprocessor
from markdown.extensions.fenced_code import FencedBlockPreprocessor
from markdown.extensions.admonition import AdmonitionProcessor

from menagerie.Items.Pages.AbstractPage import AbstractPage

__all__ = ('MDPage',)

HEADER_BORDER_CLASSES = ' border-bottom border-{{ settings[\'themes\'][\'theme-opposite\'] }} pb-1 mb-1'

ADDITIONAL_CLASSES: dict[str, str] = {
    'img': "img-fluid rounded mx-auto d-flex",
    'table': "table table-striped",
    'h1': 'border-2' + HEADER_BORDER_CLASSES,
    'h2': 'border-1' + HEADER_BORDER_CLASSES
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


def _raise_serialization_error(text):  # pragma: no cover
    raise TypeError(
        "cannot serialize {!r} (type {})".format(text, type(text).__name__)
        )


def _escape_attrib_html(text):
    # escape attribute value
    try:
        if "&" in text:
            # Only replace & when not part of an entity
            text = re.compile(r'&(?!(?:#\d+|#x[\da-f]+|[\da-z]+);)', re.I).sub('&amp;', text)
        if "<" in text:
            text = text.replace("<", "&lt;")
        if ">" in text:
            text = text.replace(">", "&gt;")
        if "\"" in text:
            text = text.replace("\"", "&quot;")
        return text
    except (TypeError, AttributeError):  # pragma: no cover
        _raise_serialization_error(text)


class MenagerieFencedCode(FencedBlockPreprocessor):

    def run(self, lines):
        if not self.checked_for_deps:
            for ext in self.md.registeredExtensions:
                if isinstance(ext, AttrListExtension):
                    self.use_attr_list = True

            self.checked_for_deps = True

        text = "\n".join(lines)
        while 1:
            m = self.FENCED_BLOCK_RE.search(text)
            if m:
                lang, id, classes, config = None, '', [], {}
                if m.group('attrs'):
                    id, classes, config = self.handle_attrs(get_attrs(m.group('attrs')))
                    if len(classes):
                        lang = classes.pop(0)
                else:
                    if m.group('lang'):
                        lang = m.group('lang')

                id_attr = lang_attr = class_attr = kv_pairs = ''
                if lang:
                    prefix = self.config.get('lang_prefix', 'language-')
                    lang_attr = f' class="{prefix}{_escape_attrib_html(lang)}"'
                if classes:
                    class_attr = f' class="{_escape_attrib_html(" ".join(classes))} position-relative"'
                else:
                    class_attr = f' class="position-relative"'
                if id:
                    id_attr = f' id="{_escape_attrib_html(id)}"'
                if self.use_attr_list and config and not config.get('use_pygments', False):
                    # Only assign key/value pairs to code element if attr_list ext is enabled, key/value pairs
                    # were defined on the code block, and the `use_pygments` key was not set to True. The
                    # `use_pygments` key could be either set to False or not defined. It is omitted from output.
                    kv_pairs = ''.join(
                        f' {k}="{_escape_attrib_html(v)}"' for k, v in config.items() if k != 'use_pygments'
                    )
                code = self._escape(m.group('code'))
                code = f'<pre{id_attr}{class_attr}><button class="menagerie-copy-button btn btn-sm btn-outline-primary position-absolute" style="top: 5px; right: 5px;" aria-label="Copy"><i class="bi bi-clipboard2"></i></button><code{lang_attr}{kv_pairs}>{code}</code></pre>'

                placeholder = self.md.htmlStash.store(code)
                text = f'{text[:m.start()]}\n{placeholder}\n{text[m.end():]}'
            else:
                break
        return text.split("\n")


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
        md.preprocessors.register(MenagerieFencedCode(md, {}), 'm-copy-button', 26)


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
