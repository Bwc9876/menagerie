---
Title: Static Files
Sort_Priority: 80
---

## Static Files

Static files are resources that pages can reference. These could be images, JS, CSS, etc.

## Adding Static Files

To add static files, simply create a new file in the `static` folder in `content`. Menagerie will auto-detect them.  
You can also create folders for these files for organization; Unlike pages, nested folders do work.

## Referencing Static Files

To reference a static file in a page, use the `static` filter.

```html
<img alt="My cool image" src="{{ '{{' }} 'images/my_image.png'|static {{ '}}' }}"/>
```

### Absolute URLs

If you need the full url for whatever reason, you can use the `full_url` filter after the static filter:

```html
<img alt="My Cool Absolute Image" src="{{ '{{' }} 'images/my_image.png'|static|full_url {{ '}}' }}"/>
```

You can also pass in a value of `False` to this filter to not prepend the `URL_PREFIX` environment variable

## Minification

JS and CSS files are minified automatically. (this can be disabled in `config.json` with the [minify]({{ 'Configuration Schema'|route }}#minify) option). You do not need to worry about
changing references to these files to `.min.js` and `.min.css`, menagerie will automatically change it. Using `.min.*`
still works, however.

## Custom Bootrstrap Themes with SASS

Menagerie supports the ability to build SASS files into CSS, it does this by looking or any file ending in `.scss` and `.sass`.  
Using this you can create a custom bootstrap theme for your site:  

1. [Get Bootstrap's source code](https://getbootstrap.com/docs/5.2/getting-started/download/#source-files) and copy the `scss` and `js` folders from it.
2. Put these folders in a new folder at the root of your docs site (next to `config.json`, we don't want it in `content` because we don't want it to build on its own).
3. Create a new static file that ends in `.scss`.
4. In this file, [customize your bootstrap theme](https://getbootstrap.com/docs/5.2/customize/sass/)
5. Import Bootstrap by referencing it (note that the path is relative to the root of your site, not the location of the file.)

    ```scss
    $primary: #00ff00;

    @import "bootstrap/scss/bootstrap";
    ```

6. In your `config.json` set your Bootstrap theme to `/path/to/your/file.min.css`

    ```json
    {
        "themes": {
            "bootstrap": "/styles/my_theme.min.css"
        }
    }
    ```

7. Generate your site!

## Images

It's recommended to use the `.webp` format for images.  
In Markdown, images will automatically get their `width` and `height` set. In HTML, you must do this yourself.

## Setting up Favicons

Menagerie will look in the folder specified in the [favicon_folder]({{ 'Configuration Schema'|route }}#brand_favicon_folder) config property, it will look for png files with specific names.  To help generate these, use this tool: [Favicon generator](https://www.favicon-generator.org/).  Make sure to select "Generate icons for Web, Android, ...".  Put the contents of the generated zip file in the `favicon_folder` folder.  You can delete `manifest.json` and `browser.config.xml` as menagerie will make these for you.
