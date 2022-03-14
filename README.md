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
Run the `bootstrap` command
```shell
python -m mgen bootstrap
```
This should create a `content/` folder as well as a `config.json`.
  
# Building

To generate the site, run the following:
```shell
python -m mgen generate
```
This will output to a folder named `out/`; to view the site open the generated `index.html` in your browser.
