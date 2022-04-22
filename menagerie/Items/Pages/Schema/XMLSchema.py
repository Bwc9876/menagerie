import re
from typing import AnyStr

from jinja2 import UndefinedError
from xmlschema import XsdElement, XMLSchema as XMLDataSchema

from menagerie.Items.Pages.AbstractPage import AbstractPage


def children(group):
    child = [child for child in group if child.__class__.__name__ == "XsdElement"]
    for child_list in [children(inner_group) for inner_group in group if inner_group.__class__.__name__ == "XsdGroup"]:
        child += child_list
    return child


def ancestry(element):
    if element.parent is None:
        return [element.name]
    else:
        if element.name is None:
            return ancestry(element.parent)
        else:
            return [element.name] + ancestry(element.parent)


NCNAME_PATTERN = re.compile(r'^[^\d\W][\w.\-]*$')


class XMLSchema(AbstractPage):

    def load_metadata(self) -> None:
        for match in re.findall(r"<!--~(.*?)~-->", self.get_content(), re.MULTILINE):
            seperated = match.strip().split(':')
            self.meta[seperated[0].lower().replace('-', '_')] = seperated[1]
        self.meta['render_toc'] = False

    base_template = 'schema_templates/schema_template.jinja2'
    extensions = ('xsd', 'xml')

    def children(self, group):
        return children(group)

    def id_path(self, element):
        return '-'.join(reversed(ancestry(element)))

    def split(self, string, delim):
        return string.split(delim)

    def get_desc(self, element: XsdElement):
        try:
            return str(element.annotation.documentation[0].text.strip())
        except (UndefinedError, AttributeError):
            return ""

    def get_name(self, obj, unnamed='none'):
        try:
            name = obj.local_name
        except AttributeError:
            try:
                obj = obj.name
            except AttributeError:
                pass
            if not isinstance(obj, str):
                return unnamed
            try:
                if obj[0] == '{':
                    _, name = obj.split('}')
                elif ':' in obj:
                    prefix, name = obj.split(':')
                    if NCNAME_PATTERN.match(prefix) is None:
                        return ''
                else:
                    name = obj
            except (IndexError, ValueError):
                return ''
        else:
            if not isinstance(name, str):
                return ''
        return name.replace('.', '_').replace('-', '_')

    def occurs_text(self, occurs):
        words = {
            0: "Zero",
            1: "One",
            None: "Many"
        }
        return "Appears " + words[occurs[0]] + " To " + words[occurs[1]] + " " + ("Time" if occurs[1] == 1 else "Times")

    def inner_render(self, content: AnyStr) -> None:
        self.manager.base_env.filters.update({
            'children': self.children,
            'id_path': self.id_path,
            'split': self.split,
            'get_desc': self.get_desc,
            'get_name': self.get_name,
            'occurs_text': self.occurs_text
        })
        schema = XMLDataSchema(content)
        return self.manager.base_env.get_template('schema_templates/xml_schema.jinja2').render(page=self, schema=schema)
