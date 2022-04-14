from json import load
from json.decoder import JSONDecodeError
from os import getenv
from pathlib import Path

from jsonschema import validate
from jsonschema.exceptions import ValidationError
from ndicts.ndicts import NestedDict

from menagerie.utils.logger import Logger

__all__ = (
    'Settings',
    'setup_settings'
)

Settings = NestedDict({
    'out_dir': None,
    'content_dir': None,
    'url_prefix': None,
    'base_url': '',
    'log_level': "Info",
    'themes': {
        'bootstrap': "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css",
        'highlight_js': "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.4.0/styles/default.min.css",
        'navbar_color': "light"
    },
    'brand': {
        'app_name': "My App",
        'short_name': "My App",
        'favicon_folder': 'images/fav/',
        'navbar_icon': None,
        'socials': [],
        'show_gen_date': True,
        'footer': {
            'show_gen_time': True,
            'show_back_to_top': True,
            'show_made_with': True,
            'links': []
        },
        'meta': {
            'description': None,
            'keywords': [],
            'categories': [],
            'image': "",
            'image_alt': "Logo",
            'theme_color': "#333333",
            'bg_color': "#ffffff"
        }
    },
    'templates': {
        'base': None,
        'table_of_contents': None,
        'schema': None
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
            'xml': True
        }
})


def setup_settings(config_path: Path):
    """
        Loads settings from a given config file and validates it against the config schema

        :param config_path: The path to the config file to load
        :type config_path: Path 
    """

    schema = load(Path('config_schema.json').open(mode='r', encoding='utf-8'))

    try:
        config = load(config_path.open(mode='r', encoding='utf-8'))
        validate(config, schema)
        Settings.update(NestedDict(config))
        Settings['out_dir'] = Path(Settings['paths', 'out'])
        Settings['content_dir'] = Path(Settings['paths', 'content'])
        Settings['url_prefix'] = getenv("URL_PREFIX", "")
        Logger.update_level_from_string(Settings['log_level'])
    except FileNotFoundError:
        Logger.log_error(f"Can't find config file: `{config_path.as_posix()}`")
    except JSONDecodeError as e:
        Logger.log_error(f"Error parsing config: {e}")
    except ValidationError as e:
        Logger.log_error(f"Invalid config: {e.message}")
