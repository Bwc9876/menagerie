---
Title: Meta Files
Sort_Priority: 40
---

# Meta Files

Meta files are special files menagerie makes for you.

!!! alert-danger "File Name Warning"
    Due to the fact these files are created at the root of the site, **please do not make any files with the same names**,
    this could break parts of the site.

## Robots.txt

Robots.txt is a file created for web crawlers to let them know what pages can and cannot be crawled.  
Any page with `Hide_In_Nav` set to True will be marked as disallowed in this list.

## Sitemap.xml

This xml file is linked in the robots.txt document and tells search engines what pages are on this site and how often to
update them.  
The priority for these items in `Sort_Priority` divided by 100.

## Manifest.webmanifest

The web manifest tells android phones what icons and color to use when adding this site to the home screen.

## Browserconfig.xml

The browser config tells Windows devices what icons and colors to use when adding a page to the start menu.

## Base.js

This js file provides common functionality like the copy button to all pages.

## Schema.js

This js file provides common functionality to schema pages such as the scroll to feature.

## Schema.css

This file provides styling to the schema page, and makes the "popout" effect that occurs when you use an anchor in the
url bar.