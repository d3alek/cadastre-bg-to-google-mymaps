#!/usr/bin/python

from argparse import ArgumentParser
import yaml
import textwrap
import tkinter as tk

def get_clipboard_text():
    root = tk.Tk()
    # keep the window from showing
    root.withdraw()
    return root.clipboard_get()

KML_FORMAT = """
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
    <Document>
%s
    </Document>
</kml>
"""

KML_PLACEMARK = """<Placemark>
    <name>{name}</name>
    <description>{description}</description>
    <Polygon>
        <extrude>1</extrude>
        <altitudeMode>relativeToGround</altitudeMode>
        <outerBoundaryIs>
            <LinearRing>
                <coordinates>
{coordinates} 
                </coordinates>
            </LinearRing>
        </outerBoundaryIs>
    </Polygon>
</Placemark>"""

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    parser = ArgumentParser()
    parser.add_argument('--input', '-i', help='Path to yaml file manually written from kais.cadastre.bg data')
    parser.add_argument('output', help='Path to output the KML file ready to import into Google My Maps')

    args = parser.parse_args()

    if args.input:
        with open(args.input) as f:
            data = yaml.load(f)
    else:
        # use text in clipboard
        data = yaml.load(get_clipboard_text())

    placemarks = []
    for land in data:
        coordinates = land['edges']
        placemarks.append(
                KML_PLACEMARK.format(
                    name=land['name'], 
                    size_dka=int(land.get('size',0))/1000,
                    description=land.get('description',''),
                    coordinates=textwrap.indent(coordinates, 20*' ')))

    with open(args.output, 'w') as f:
        f.write(KML_FORMAT % textwrap.indent('\n'.join(placemarks), 8*' '))

    print("Written %d lands to %s." % (len(placemarks), args.output))

