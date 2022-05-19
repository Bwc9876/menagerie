import sass

from menagerie.Items.Static.StaticCSS import StaticCSS



class StaticSCSS(StaticCSS):
    extensions = ('scss', 'sass')
    
    def transform(self, content: str) -> str:
        return sass.compile(string=content)

