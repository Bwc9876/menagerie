# Menagerie

A static site generator that supports:

- Markdown
- HTML
- JSON Schemas (Limited)
- XML Schemas
- YAML Schemas (Coming soon)

# Setup

Install the package via your favorite virtual environment manager:

```shell
pipenv install menagerie-docs
```

Run the `start_project` command

```shell
python -m menagerie start_project MySite
```

This will create a `content/` folder as well as a `config.json` within a folder called `MySite`.

Also, you may want to add `./m_cache` to your .gitignore

# Building

To generate the site, run the following:

```shell
python -m menagerie generate
```

This will output to a folder named `out/`; to view the site open the generated `index.html` in your browser.

## Custom Config Path

```shell
python -m menagerie generate --config=PATH/TO/CONFIG
```
