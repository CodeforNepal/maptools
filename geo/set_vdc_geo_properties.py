import getopt
import json
import sys

'''
Script to manipulate the properties of each VDC in the vdc.geojson file
in the goe repository and convert each to the format needed for NepalMap
'''


def convert_csv(input_file, output_file):
    with open(input_file, 'r') as data_file:
        data = json.load(data_file)

        def build_wazimap_feature(feature):
            old_type = feature['type']
            old_geometry = feature['geometry']
            old_properties = feature['properties']
            code = old_properties['ID_4']
            name = old_properties['NAME_4']
            new_properties = {
                'code': code,
                'name': name,
                'geoid': '{}-{}'.format(code,
                                        name.replace(' ', '-').replace('.',
                                                                       '')),
                'level': 'vdc'
            }
            return {
                'type': old_type,
                'geometry': old_geometry,
                'properties': new_properties
            }

        features = list(map(lambda f: build_wazimap_feature(f),
                              data['features']))

        len(features)
        new_collection = dict(type=data['type'], features=features)
        
        with open(output_file, 'w') as json_out:
            json.dump(new_collection, json_out, ensure_ascii=False)

    print('Done!')


def main(args):
    indir = ''
    outputjson = ''
    try:
        opts, args = getopt.getopt(args, 'hi:o:',
                                   ['indir=', 'outputjson='])
    except getopt.GetoptError:
        print('python set_vdc_geo_properties.py -i <indir> -o <outputjson>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('python set_vdc_geo_properties.py -i <indir> '
                  '-o <outputjson>')
            sys.exit()
        elif opt in ('-i', '--indir'):
            indir = arg
        elif opt in ('-o', '--outputjson'):
            outputjson = arg

    convert_csv(indir, outputjson)


if __name__ == '__main__':
    main(sys.argv[1:])
