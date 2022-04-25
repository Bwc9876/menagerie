import importlib.resources as pkg_resources
from json import load, loads
from json.decoder import JSONDecodeError
from os import getenv
from pathlib import Path

from jsonschema import validate
from jsonschema.exceptions import ValidationError
from ndicts.ndicts import NestedDict

from menagerie import schemas
from menagerie.utils.logger import Logger

__all__ = (
    'Settings',
    'setup_settings'
)

Settings = NestedDict({
    'config_path': None,
    'out_dir': None,
    'content_dir': None,
    'url_prefix': None,
    'default-toc': True,
    'base_url': '',
    'cache_enabled': True,
    'log_level': "Info",
    'themes': {
        'bootstrap': "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css",
        'highlight_js': "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.4.0/styles/default.min.css",
        'theme': "light"
    },
    'brand': {
        'app_name': "My App",
        'short_name': "My App",
        'favicon_folder': 'images/fav/',
        'navbar_icon': None,
        'navbar_icon_size': (100, 100),
        'socials': [],
        'show_gen_date': True,
        'footer': {
            'show_gen_time': True,
            'show_back_to_top': True,
            'show_made_with': True,
            'links': []
        },
        'meta': {
            'description': "",
            'keywords': [],
            'categories': [],
            'image': "",
            'image_alt': "Logo",
            'theme_color': "#333333",
            'bg_color': "#ffffff"
        }
    },
    'styles': {
        'base': None,
        'schema': None
    },
    'paths': {
        'out': "out/",
        'content': 'content/',
        'pages': 'pages/',
        'static': 'static/',
        'cache': '.m_cache/'
    },
    'minify':
        {
            'html': True,
            'css': True,
            'js': True,
            'xml': True,
            'json': True
        }
})


def setup_settings(config_path: Path):
    """
        Loads settings from a given config file and validates it against the config schema

        :param config_path: The path to the config file to load
        :type config_path: Path 
    """

    schema = loads(pkg_resources.read_text(schemas, 'config_schema.json'))

    try:
        config = loads(config_path.read_text(encoding='utf-8'))
        validate(instance=config, schema=schema)
        new_config = Settings.copy()
        new_config.update(NestedDict(config))
        new_config['out_dir'] = Path(new_config['paths', 'out'])
        new_config['content_dir'] = Path(new_config['paths', 'content'])
        new_config['url_prefix'] = getenv("URL_PREFIX", "")
        new_config['config_path'] = config_path
        Logger.update_level_from_string(new_config['log_level'])
        return new_config
    except FileNotFoundError:
        Logger.log_error(f"Can't find config file: `{config_path.as_posix()}`")
    except JSONDecodeError as e:
        Logger.log_error(f"Error parsing config: {e}")
    except ValidationError as e:
        Logger.log_error(f"Invalid config: {e.message}")
