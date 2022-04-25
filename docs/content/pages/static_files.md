Title: Static Files
Sort_Priority: 80

# Static Files

Static files are resources that pages can reference. These could be images, JS, CSS, etc.

# Adding Static Files

To add static files, simply create a new file in the `static` folder in `content`. Menagerie will auto-detect them.  
You can also create folders for these files for organization; Unlike pages, nested folders do work.

# Referencing Static Files

To reference a static file in a page, use the `static` filter.

```html
<img alt="My cool image" src="{{ '{{' }} 'images/my_image.png'|static {{ '}}' }}"/>
```

## Absolute URLs

If you need the full url for whatever reason, you can use the `full_url` filter after the static filter:

```html
<img alt="My Cool Absolute Image" src="{{ '{{' }} 'images/my_image.png'|static|full_url {{ '}}' }}"/>
```

You can also pass in a value of `False` to this filter to not prepend the `URL_PREFIX` environment variable

# Minification

JS and CSS files are minimizes automatically. (this can be disabled in `config.json`). You do not need to worry about
changing references to these files to `.min.js` and `.min.css`, menagerie will automatically change it. Using `.min.*`
still works, however.

# Images

It's recommended to use the `.webp` format for images.

# Setting up Favicons

Menagerie will look in the folder specified in the `favicon_folder` config property, it will look for png files with specific names.  To help generate these, use this tool: [Favicon generator](https://www.favicon-generator.org/).  Make sure to select "Generate icons for Web, Android, ...".  Put the contents of the generated zip file in the `favicon_folder` folder.  You can delete `manifest.json` and `browser.config.xml` as menagerie will make these for you. 
