Title: Home
Sort-Priority: 100
Render_TOC: True

# Menagerie Docs

Menagerie docs is a python package used to generate static sites from a *menagerie* (see what I did there?) of files

# Installation

To get started, install `menagerie_docs` with your package manager

```shell
pip install menagerie_docs
```

# Starting a project

Once installed, you can use the `new-project` command

```shell
python -m menagerie new-project MyCoolDocsSite
```

This will create a new folder called `MyCoolDocsSite` with the following contents:

```file
- content/
    - pages/
        - index.md
    - static/
- config.json
```

# Next steps

Now you're ready to start creating your site!  
For help with this, look at the rest of this site, the [pages]({{ "pages"|route }}) page is a good place to start
