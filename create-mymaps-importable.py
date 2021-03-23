#!/usr/bin/python

from argparse import ArgumentParser
import yaml
import subprocess
from pathlib import Path
import textwrap

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
    <description>{size_dka} дка
    {description}
    </description>
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

def call_cs2cs(wgs_utm_32n_coordinates):
    """
    >>> call_cs2cs("4747080 309559")
    '24.669154,42.852584'
    >>> call_cs2cs("4747080.30 309559")
    '24.669154,42.852587'
    """
    cwd = Path(__file__).parents[0].absolute()
    split = wgs_utm_32n_coordinates.split(' ')
    if len(split) != 2:
        return ''
    result = subprocess.run([str(cwd)+'/cs2cs-cadastre-to-maps.sh', split[0], split[1]], stdout=subprocess.PIPE)
    result_split = str(result.stdout, 'utf-8').split('\t')
    return result_split[0] + ',' + result_split[1].split(' ')[0]

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    parser = ArgumentParser()
    parser.add_argument('input_file', help='Path to yaml file manually written from kais.cadastre.bg data')
    parser.add_argument('output_file', help='Path to output the KML file ready to import into Google My Maps')

    args = parser.parse_args()

    with open(args.input_file) as f:
        data = yaml.load(f)

    placemarks = []
    for land in data:
        coordinates = '\n'.join(map(call_cs2cs, land['edges'].splitlines()))
        placemarks.append(
                KML_PLACEMARK.format(
                    name=land['name'], 
                    size_dka=int(land['size'])/1000,
                    description=land.get('description',''),
                    coordinates=textwrap.indent(coordinates, 20*' ')))

    with open(args.output_file, 'w') as f:
        f.write(KML_FORMAT % textwrap.indent('\n'.join(placemarks), 8*' '))

    print("Written %d lands to %s." % (len(placemarks), args.output_file))

