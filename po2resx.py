#!/usr/bin/env python
#
import argparse
import json
import os
from xml.sax.saxutils import escape

import jinja2
import polib


# Utilities
def escape_xml(text):
    '''
    Escape the following characters: < > & ' '
    '''
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


def load_keys(path):
    with open(path, 'rb') as jsonfile:
        return json.loads(jsonfile.read())


def write_file(content, path):
    with open(path, 'wb') as output:
        output.write(content.encode('utf8'))


# Key Generation
def get_keys(entries):
    keys = dict([(entry['key'], 'SET_KEY_HERE') for entry in entries])
    return json.dumps(
        keys,
        indent=4,
    )


def get_keyfile_path(input_path):
    parent_path, input_file = os.path.split(input_path)
    input_filename, ext = os.path.splitext(input_file)
    output_filename = 'keys.json'
    return os.path.join(parent_path, output_filename)


def generate_keyfile(po_path):
    entries = load_po(po_path)
    keys = get_keys(entries)
    keyfile_path = get_keyfile_path(po_path)
    write_file(keys, keyfile_path)


# PO Conversion
def label_entries(entries, keys):
    return [{
        'key': keys[entry['key']],
        'value': entry['value'],
    } for entry in entries]


def render_xml(entries):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))
    template = env.get_template('resx_template.xml')
    return template.render(entries=entries)


def get_output_path(input_path):
    parent_path, input_file = os.path.split(input_path)
    input_filename, ext = os.path.splitext(input_file)
    output_filename = '{name}.resx'.format(name=input_filename)
    return os.path.join(parent_path, output_filename)


def convert_po_to_resx(po_path, key_path, output):
    entries = load_po(po_path)
    keys = load_keys(key_path)
    labeled_entries = label_entries(entries, keys)
    xml = render_xml(labeled_entries)
    resx_path = output or get_output_path(po_path)
    write_file(xml, resx_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convert a PO file to a Microsoft RESX file.')
    parser.add_argument(
        'command',
        help='The command to execute.',
        choices=('makekeys', 'convert'),
    )
    parser.add_argument(
        '-pofile',
        help='The path to the input PO file.',
    )
    parser.add_argument(
        '-keyfile',
        help='The path to the key file for conversion.',
    )
    parser.add_argument(
        '-output',
        help='An optional path to the output file.',
    )
    args = parser.parse_args()

    if args.command == 'makekeys':
        generate_keyfile(args.pofile)
    elif args.command == 'convert':
        convert_po_to_resx(args.pofile, args.keyfile, output=args.output)
