Title: Pages
Sort_Priority: 90

# Pages

Pages are the actual content the user sees. The page you're currently looking at is a [markdown page](https://github.com/Bwc9876/menagerie/blob/master/docs/content/pages/pages.md){target='_blank'}.

# Adding Pages

To create new pages, simply add them to the `pages` folder in `content`.  
Menagerie will look for the following file extensions to generate from:

```diff
+ *.md -> Markdown
+ *.jinja2, *.html, *.htm -> HTML
+ *.json, *.jsonc -> JSON Schema
+ *.xsd, *.xml -> XML Schema
- *.yml -> YAML Schema (Support coming soon)
```

# Page Metadata

Page metadata is data included in the file that tells menagerie how to generate a corresponding HTML document.  
The way to describe metadata is different depending on what language you're using

## Markdown Metadata

Uses the standard markdown metadata format, create a block at the very top of your document that looks like this:

```md
Title: My Page
Sort-Priority: 100
```

## HTML Metadata

Uses **jinja** comments (`{{ '{#' }} {{ '#}' }}`), create comments near the top of the file that look like this (note the `~` characters):

```jinja2
{{ '{#~' }} Title: My Page {{ '~#}' }}
{{ '{#~' }} Sort-Priority: {{ '~#}' }}
```

## JSON Schema Metadata

Create a top-level key named `$docs`. Then simply put in keys:

```jsonc
{
    // ...
    "$docs": {
        "title": "My Page",
        "sort_priority": 100
    }
    // ...
}
```

## XML Schema Metadata

Uses xml comments; create comments near the top of the file that look like this (note the `~` characters)

```xml
<!--~ Title:My Page ~-->
<!--~ Sort_Priority:100 ~-->
<Myelement>Text</Myelement>
<!-- ... -->
```

# Metadata Reference

| **Name**          | **Description**                                                                                                                                                           | **Default**                                  |
|-------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------|
| **Title**         | The title of this page, displayed in many places and used in metadata. Also what you pass to `route`.  This is case-insensitive so make sure not to make duplicate titles | Derives from filename if nothing is provided |
| **Description**   | The description of this page, appears in social media embeds and metadata                                                                                                 | Description specified in `config.json`       |
| **Sort_Priority** | How much to prioritize this page in the navbar, should be from 0-100.                                                                                                     | 30                                           |
| **Render_TOC**    | Whether to render a table of contents on this page (HTML/MD Pages only)                                                                                                   | True                                         |
| **Out_File**      | Name of output file, omit the file extension                                                                                                                              | Same as name of source file                  |

# Linking to Pages

You can link to other pages in markdown and html pages by using the `route` filter and passing in the title of the page

```jinja2
<a href="{{ '{{' }} 'my page'|route {{ '}}' }}">Check out my cool page!</a>
```

```md
[Check out my cool page!]({{ '{{' }} 'my page'|route {{ '}}' }})
```

# Table of Contents

A table of contents is automatically generated for HTML and Markdown pages.  
This can be disabled with the `render_toc` metadata attribute.

## In Markdown

In markdown all headings are put into the table of contents

## In HTML

In HTML all headings **with an id** are put into the table of contents

# Images

Images are [static files]({{ "static files"|route }}), in order to get the path to put in the src attribute, you can use the `static` filter. Pass in the path of the files relative to the `static` folder in `content`.

```jinja2
<img alt="My cool image" src="{{ '{{' }} 'images/my_image.png'|static {{ '}}' }}"/>
```

```md
![My cool image]({{ '{{' }} 'images/my_image.png'|static {{ '}}' }})
```

# Adding Styles to Pages

You can use the `styles` config option to set a global CSS file to apply to all pages, just pass in the path relative to the `static` folder.

```jsonc
{
    // ...
    "styles": {
        "base": "styles/my_base_styles.css",
        "schema": "styles/my_schema_styles.css" // You can also specify one for schemas only
    }
    // ...
}
```

# Grouping Pages

To create groups of pages (dropdowns in the navbar), create folders in the `pages` folder. For example if I want a dropdown for all of my schemas I might lay out my `pages` folder like so:

```file
- index.md
- schemas/
    - my_schema.json
    - my_other_schema.xsd
```

This will create a dropdown named "Schemas" on the navbar.  

## Group Metadata

Groups can also have metadata.  To specify it, create a file called `_folder.json` in the folder.  Then fill this out with the metadata.  Groups only allow for `title` and `sort_priority` to be set.

# Minification

All rendered pages are minified to save on space and network load (this can be disabled in `config.json`).
