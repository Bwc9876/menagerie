# Menagerie

A static site generator that supports:

- Markdown
- HTML
- JSON Schemas
- XML Schemas
- YAML Schemas

# Setup

Install the package via your favorite virtual environment manager:

```shell
pipenv install menagerie-docs
```

Run the `start` command

```shell
python -m mgen start MySite/
```

This will create a `content/` folder as well as a `config.json` within a folder called `MySite`.  
Omit the path to have it create these files in the working dir.

# Building

To generate the site, run the following:

```shell
python -m mgen generate
```

This will output to a folder named `out/`; to view the site open the generated `index.html` in your browser.

## Custom Config Path

```shell
python -m mgen generate --config=PATH/TO/CONFIG
```
