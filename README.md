# html-safe

Proof-of-concept encrypted vault implemented as an editable HTML file.

## Features

This provides a printable password-protected HTML note with the following editable fields:
- **Title:** used as the HTML document title (not encrypted) and main header for the note.
- **Main text:** formatted content displayed centralized right below the title.
- **Codes:** text field for a list of codes, displayed in a mono-spaced font with multiple columns.
- **Notes:** additional formatted field, displayed at the bottom with mono-spaced font.

## How to use

Opening an empty vault file in the browser will display a form to edit the note and set its password. 

Saving the note will display the edited contents and also allow printing. 

- **WARNING:** at this point, the changes are NOT PERSISTED YET, reloading the page will erase them.

Locking the note will erase all clear-text content, leaving only the password-protected encrypted data behind. Once locked, to view the contents requires unlocking the note with the original password.

Once the note is locked, the changes can be persisted using the "Download" button. Which will download a new HTML file with the persisted encrypted contents.

The note can also be saved using the browser's "Save As" feature. It may be required to save it as a "complete HTML page" for the actual changes to be saved (and not just a copy of the original file).

- **WARNING:** if using "Save As" to save the changes, ONLY SAVE WHEN THE PAGE IS LOCKED, otherwise you will be saving the clear-text content in the resulting file.

The resulting file can be opened in the browser and unlocked with the password. The contents can be further edited and the changes saved using the above procedures (either by downloading a new file or using "Save As").

## How it works

The basic idea is to create a self-contained HTML file that can be edited 
by the user and have its contents encrypted by a password. The whole file
can then be saved and will safely store the user-edited content encrypted.

The editing is done trivially by using the [`contenteditable`](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/contentEditable)
attribute. This allows for formatted text, including images which can be
inserted by copy-and-paste. Additional structured content can be edited
using a plain HTML form.

The edited HTML content is then encrypted using the [Web Crypto API](https://developer.mozilla.org/en-US/docs/Web/API/Crypto)
and saved as part of the DOM as a hidden element, while the original content
is removed from the page.

The HTML page can then be saved (in Chrome it requires saving as a complete
page). The saved page will retain the modified DOM with the encrypted user
content. Alternatively, the provided download button will create a local
[Data URI](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URIs)
link and use it to download the HTML file.

Opening the modified file, the user content can be loaded by providing the
same password. This will decrypt the HTML content and insert it into the page
where it can be viewed or edited further.
