#!/usr/bin/env python3

import argparse
import os
import yaml

from expressionive.expressionive import htmltags as T
import expressionive.expressionive as xpres

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", "-o")
    parser.add_argument("--box", action='store_true')
    parser.add_argument("--png", action='store_true')
    parser.add_argument("--html", action='store_true')
    parser.add_argument("definitions_file")
    return vars(parser.parse_args())

def filename(name):
    return name.replace(' ', '-')

def make_keycaps(definitions_file, outdir, png=False, html=False, box=False):
    os.makedirs(outdir, exist_ok=True)
    size = "16px"
    right = "128"
    bottom = "128"
    with open(definitions_file) as instream:
        definitions = yaml.safe_load(instream)
        for name, definition in definitions['keycaps'].items():
            output_name = os.path.join(outdir, filename(name))
            with open(output_name + ".svg", 'w') as o:
                o.write('<svg width="%s" height="%s">\n' % (right, bottom))
                if box:
                    o.write('  <rect x="0" y="0" width="%s" height="%s" fill="none" stroke="red" stroke-width="2"/>\n' % (right, bottom))
                for part in definition:
                    size = "16px"
                    right = "128"
                    bottom = "128"
                    default_x = 16
                    default_y = 16
                    x = default_x
                    y = default_y
                    text_line = None
                    for action, arg in part.items():
                        match action:
                            case 'font-size':
                                size = arg
                            case 'x':
                                x = default_x + int(arg)
                            case 'y':
                                y = default_y + int(arg)
                            case 'text':
                                text_line = arg
                    if text_line:
                        o.write('  <text font-size="%s" x="%d" y="%d">%s</text>\n' % (size, x, y, text_line))
                o.write('</svg>\n')
            if png:
                os.system("convert %s.svg %s.png" % (output_name, output_name))
        if html and 'grid' in definitions:
            style_text = ""
            script_text = ""
            with open(os.path.join(outdir, "grid.html"), 'w') as page:
                page.write(
                    xpres.Serializer(xpres.examples_vmap, 'utf-8').serialize(
                        xpres.HTML5Doc(body=T.html[
                                           T.table[
                                               [[T.tr[[T.td[T.p[keycap],
                                                            T.img(src=filename(keycap) + ".png")
                                                            ] for keycap in row]]]
                                                for row in definitions['grid']]]],
                                       head=T.head[T.meta(charset='utf-8'),
                                                   T.title["Keycaps"]],
                                       )))

if __name__ == "__main__":
    make_keycaps(**get_args())
