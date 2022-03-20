import re

from Items.Pages.AbstractPage import AbstractPage

__all__ = ('HTMLPage',)


class HTMLPage(AbstractPage):
    extensions = ('jinja2', 'html', 'html5', 'htm')

    def inner_render(self, content: str) -> str:
        return self.manager.env.from_string(content).render(page=self, **self.manager.context)

    def load_metadata(self):
        for match in re.findall(r"{#~(.*?)~#}", self.get_content(), re.MULTILINE):
            seperated = match.strip().split(':')
            self.meta[seperated[0].lower().replace('-', '_')] = seperated[1]
