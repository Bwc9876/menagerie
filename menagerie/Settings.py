from json.decoder import JSONDecodeError
from pathlib import Path
from json import load

from jsonschema import validate
from jsonschema.exceptions import ValidationError

from utils.logger import Logger


class Settings:
    base_url: str = None
    log_level: str = 'info',
    themes = {
        'bootstrap': "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css",
        'highlight_js': "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.4.0/styles/default.min.css"
    },
    brand = {
        'app_name': "My App",
        'favicon_folder': None,
        'navbar_icon': None,
        'socials': [],
        'show_gen_date': True,
        'footer_links': [],
        'meta': {
            'description': None,
            'keywords': [],
            'image': None,
            'image_alt': "Logo",
            'theme_color': "#080808",
            'bg_color': "#ffffff"
        }
    },
    templates = {
        'base': None,
        'table_of_contents': None,
        'schema': None
    },
    styles = {
        'base': None,
        'schema': None
    }
    default_toc = True
    folders = {
        'out': "out/",
        'content': 'content/',
        'pages': 'pages/',
        'static': 'static/'
    }
    minify = {
        'html': True,
        'css': True,
        'js': True,
        'xml': True
    }

    


def setup_settings(config_path: Path):


    schema = load(Path('config_schema.json'))

    try:
        config = load(config_path)
        validate(config, schema)
        Settings.__dict__.update(config)
        Logger.update_level_from_string(Settings.log_level)
    except FileNotFoundError:
        Logger.log_error(f"Can't find config file: `{config_path.as_posix()}`")
    except JSONDecodeError as e:
        Logger.log_error(f"Error parsing config: {e}")
    except ValidationError as e:
        Logger.log_error(f"Invalid config: {e.message}")

    