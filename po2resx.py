import os
from xml.sax.saxutils import escape

import jinja2
import polib


def escape_xml(text):
    """
    Escape the following characters: < > & ' "
    """
    return escape(text, {
        '\'': '&apos;',
        '"': '&quot;',
    })


def load_po(path):
    pofile = polib.pofile(path)
    return [{
        'key': entry.msgid,
        'value': entry.msgstr
    } for entry in pofile]


def render_xml(entries):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader("."))
    template = env.get_template('resx_template.xml')
    return template.render(entries=entries)


def get_output_path(input_path):
    parent_path, input_file = os.path.split(input_path)
    input_filename, ext = os.path.splitext(input_file)
    output_filename = '{name}.resx'.format(name=input_filename)
    return os.path.join(parent_path, output_filename)


def write_file(content, path):
    with open(path, 'wb') as output:
        output.write(content.encode('utf8'))


def convert_po_to_resx(po_path):
    entries = load_po(po_path)
    xml = render_xml(entries)
    resx_path = get_output_path(po_path)
    write_file(xml, resx_path)
