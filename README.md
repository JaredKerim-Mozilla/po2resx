# po2resx 

**Convert PO translation files into Microsoft resx format**

# Overview

Automate the conversion of PO translation files, used in Django projects,
into the resx XML format used by .NET projects.

# Requirements

* Python (2.6.5+, 2.7, 3.2, 3.3, 3.4)
* Jinja 2.7.3
* polib 1.0.5

# Usage 

## Create a key file

In a Django PO file, translations are identified by the original text content
found in the code or template, for example:

    msgid "Your payment is complete."
    msgstr "Votre paiement est terminé."

However, in a .NET project, translations are identified with a unique identifier,
so we must create a mapping from the unique identifier to the native language
string.  To do that we create a key file:

    python po2resx.py makekeys -pofile messages.po

This will create a file called keys.json

## Set unique identifiers 

In the newly created keys.json you will find a JSON dictionary which maps
the native language text of each entry in your PO file to the placeholder 
"SET_KEY_HERE".

Replace each instance of SET_KEY_HERE to the desired identifier for each
translation string.

## Convert your PO file to a resx

Now that you've created a key file, you can use it to create the desired
resx file:

    python po2resx.py convert -pofile messages.po -keyfile keys.json -output messages.resx
