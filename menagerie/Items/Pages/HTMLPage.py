import re

from bs4 import BeautifulSoup

from menagerie.Items.Pages.AbstractPage import AbstractPage

__all__ = ('HTMLPage',)

HEADER_PATTERN = re.compile('^h[1-6]$')


class HTMLPage(AbstractPage):
    extensions = ('jinja2', 'html', 'html5', 'htm')

    def inner_render(self, content: str) -> str:
        return self.manager.env.from_string(content).render(page=self, **self.manager.context)

    def setup_toc(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        toc_raw = []
        for match in soup.find_all(HEADER_PATTERN):
            if 'id' in match.attrs.keys():
                toc_raw.append({
                    'level': int(match.name[1]),
                    'id': match['id'],
                    'name': match.text,
                    'parent': None,
                    'children': []
                })
        root = []
        current_scope = root
        current_parent = None
        current_level = 1
        for index, item in enumerate(toc_raw):
            if item['level'] > current_level:
                current_parent = toc_raw[index - 1]
                current_level = item['level']
                current_scope = current_parent['children']
            elif item['level'] < current_level:
                curr_p = toc_raw[index - 1]
                while curr_p['level'] != item['level']:
                    curr_p = curr_p['parent']
                current_parent = curr_p['parent']
                current_scope = current_parent['children'] if current_parent is not None else root
                current_level = item['level']

            current_scope.append(item)
            item['parent'] = current_parent
        self.meta['table_of_contents'] = root

    def load_metadata(self):
        content = self.get_content()
        for match in re.findall(r"{#~(.*?)~#}", content, re.MULTILINE):
            seperated = match.strip().split(':')
            self.meta[seperated[0].lower().replace('-', '_')] = seperated[1]
        if self.meta['render_toc']:
            self.setup_toc(content)


