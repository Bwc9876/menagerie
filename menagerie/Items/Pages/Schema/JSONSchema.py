from json import JSONDecoder, JSONDecodeError

from json_schema_for_humans.generate import generate_schemas_doc
from json_schema_for_humans.generation_configuration import GenerationConfiguration
from json_schema_for_humans.schema.schema_to_render import SchemaToRender
from json_schema_for_humans.template_renderer import TemplateRenderer

from menagerie.Items.Pages.AbstractPage import AbstractPage
from menagerie.utils.logger import Logger
from menagerie.utils.no_print import NoPrint

SCHEMA_SETTINGS = GenerationConfiguration()
SCHEMA_SETTINGS.link_to_reused_ref = False
SCHEMA_SETTINGS.minify = False


class JSONSchema(AbstractPage):
    base_template = 'schema_templates/schema_template.jinja2'
    extensions = ('json', 'jsonc')

    def load_metadata(self) -> None:
        try:
            decoded = JSONDecoder().decode(self.get_content())
            self.meta.update({k.strip().lower(): v for k, v in decoded.get("$docs", {}).items()})
        except JSONDecodeError as jde:
            Logger.log_error(f"Couldn't parse json file: {self.in_path.name}: {str(jde)}")

    def inner_render(self, content: str) -> str:
        schema_renderer = TemplateRenderer(SCHEMA_SETTINGS)
        self.manager.base_env.filters.update(schema_renderer.template.environment.filters)
        self.manager.base_env.tests.update(schema_renderer.template.environment.tests)
        self.manager.base_env.globals.update(schema_renderer.template.environment.globals)
        schemas = [SchemaToRender(self.get_path_to_open(), None, None)]
        schema_template = self.manager.base_env.get_template("schema_templates/json/schema_base.jinja2")
        template_renderer = TemplateRenderer(SCHEMA_SETTINGS, schema_template)
        template_renderer.render = lambda inter: self.template_override(template_renderer, inter,
                                                                        **self.manager.context)
        with NoPrint():
            rendered = generate_schemas_doc(schemas, template_renderer)
        return rendered[str(self.in_path.name)]

    def template_override(self, template: TemplateRenderer, intermediate_schema, **context):
        template.template.environment.loader = self.manager.base_env.loader
        rendered = template.template.render(schema=intermediate_schema, config=SCHEMA_SETTINGS,
                                            title=self.meta['title'], **context)
        return rendered
