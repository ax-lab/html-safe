# html-safe

Proof-of-concept encrypted vault implemented as an editable HTML file.

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
