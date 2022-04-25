Title: Home
Sort_Priority: 100
Render_TOC: True

# Menagerie Docs

Menagerie docs is a python package used to generate static sites from a *menagerie* (see what I did there?) of files.

# Installation

To get started, install `menagerie-docs` with your package manager.

```shell
pip install menagerie-docs
```

# Starting a project

Once installed, you can use the `new-project` command.

```shell
menagerie new-project MyCoolDocsSite
```

This will create a new folder called `MyCoolDocsSite` with the following contents:

```txt
- content/
    - pages/
        - index.md
    - static/
- config.json
```

# Generating the site

To generate the site, run the `generate` command.

```shell
menagerie generate
```

You can also specify a different config file by passing it in as an arg.

```shell
menagerie generate my-config.json
```

# Next steps

Now you're ready to start creating your site!  
For help with this, look at the rest of this site, the [pages]({{ "pages"|route }}) page is a good place to start.  
In addition, [this site was generated in menagerie](https://github.com/Bwc9876/menagerie/tree/master/docs){target="_blank"}, so you can use it as an example.
