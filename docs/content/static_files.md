Title: Static Files
Sort_Priority: 80

# Static Files

Static files are resources that pages can reference.  These could be images, JS, CSS, etc.

# Adding Static Files

To add static files, simply create a new file in the `static` folder in `content`.  Menagerie will auto-detect them.  
You can also create folders for these files for organization; Unlike pages, nested folders do work.

# Referencing Static Files

To reference a static file in a page, use the `static` filter.

```jinja2
<img alt="My cool image" src="{{ '{{' }} 'images/my_image.png'|static {{ '}}' }}"/>
```

## Absolute URLs

If you need the full url for whatever reason, you can use the `full_url` filter after the static filter:

```jinja2
<img alt="My Cool Absolute Image" src="{{ '{{' }} 'images/my_image.png'|static|full_url {{ '}}' }}"/>
```

# Minification

JS and CSS files are minimizes automatically. (this can be disabled in `config.json`).  You do not need to worry about changing references to these files to `.min.js` and `.min.css`, menagerie will automatically change it. Using `.min.*` still works however.

# Images

It's recommended to use the `.webp` format for images, support for auto-converting to this can come soon.

