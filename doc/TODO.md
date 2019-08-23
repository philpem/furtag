# TODO list

- base template:
    - when logged out, "not logged in" should be a clickable "Log In" link
- base template and core:
    - menu items should have a "visible when logged out" attribute
    - "dashboard (logged out)" text should not be shown, show menu items instead
- database: implement data model
    - Digital Artefacts (files) -> id, sha512, filename, description/notes, allow download
    - Physical Artefacts -> id, title, notes, location
    - Web Links -> id, title, url
    - People -> id, name, weblink
    - Companies -> id, name, weblink		[Company can link to People]
    - Categories -> id, name
    - Product -> id, name, description	[1..n: categories, 1..n: people, 1..n: companies{+role - dev, pub, ...; +year} ]
- weblinks:
    - intersite linking via URL or generator (e.g. 'qubeserver:/Commercial Apps/ADF' links to qubeserver.com FTP)
- templates:
    - update Bootstrap
    - load Bootstrap from a CDN (?)
    - use Typeahead for search autocomplete
- Pass database config through as an ENV variable (Docker builds)
    - To make Archivist easier to use with Docker

