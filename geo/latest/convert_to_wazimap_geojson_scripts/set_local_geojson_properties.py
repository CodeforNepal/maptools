import getopt
import json
import re
import sys

'''
Script to manipulate the properties of each Local in the local_fix.geojson file
in the geo repository and convert each to the format needed for NepalMap output as local.geojson
'''

district_rel = [{'Achham': 'dis-01'}, {'Arghakhanchi': 'dis-02'}, {'Baglung': 'dis-03'}, {'Baitadi': 'dis-04'}, {'Bajhang': 'dis-05'}, {'Bajura': 'dis-06'}, {'Banke': 'dis-07'}, {'Bara': 'dis-08'}, {'Bardiya': 'dis-09'}, {'Bhaktapur': 'dis-10'}, {'Bhojpur': 'dis-11'}, {'Chitawan': 'dis-12'}, {'Dadeldhura': 'dis-13'}, {'Dailekh': 'dis-14'}, {'Dang': 'dis-15'}, {'Darchula': 'dis-16'}, {'Dhading': 'dis-17'}, {'Dhankuta': 'dis-18'}, {'Dhanusha': 'dis-19'}, {'Dolakha': 'dis-20'}, {'Dolpa': 'dis-21'}, {'Doti': 'dis-22'}, {'Gorkha': 'dis-23'}, {'Gulmi': 'dis-24'}, {'Humla': 'dis-25'}, {'Ilam': 'dis-26'}, {'Jajarkot': 'dis-27'}, {'Jhapa': 'dis-28'}, {'Jumla': 'dis-29'}, {'Kailali': 'dis-30'}, {'Kalikot': 'dis-31'}, {'Kanchanpur': 'dis-32'}, {'Kapilbastu': 'dis-33'}, {'Kaski': 'dis-34'}, {'Kathmandu': 'dis-35'}, {'Kabhrepalanchok': 'dis-36'}, {'Khotang': 'dis-37'}, {'Lalitpur': 'dis-38'}, {'Lamjung': 'dis-39'}, {'Mahottari': 'dis-40'}, {'Makawanpur': 'dis-41'}, {'Manang': 'dis-42'}, {'Morang': 'dis-43'}, {'Mugu': 'dis-44'}, {'Mustang': 'dis-45'}, {'Myagdi': 'dis-46'}, {'Nawalparasi_E': 'dis-47'}, {'Nuwakot': 'dis-48'}, {'Okhaldhunga': 'dis-49'}, {'Palpa': 'dis-50'}, {'Panchthar': 'dis-51'}, {'Parbat': 'dis-52'}, {'Parsa': 'dis-53'}, {'Pyuthan': 'dis-54'}, {'Ramechhap': 'dis-55'}, {'Rasuwa': 'dis-56'}, {'Rautahat': 'dis-57'}, {'Rolpa': 'dis-58'}, {'Rukum_E': 'dis-59'}, {'Rupandehi': 'dis-60'}, {'Salyan': 'dis-61'}, {'Sankhuwasabha': 'dis-62'}, {'Saptari': 'dis-63'}, {'Sarlahi': 'dis-64'}, {'Sindhuli': 'dis-65'}, {'Sindhupalchok': 'dis-66'}, {'Siraha': 'dis-67'}, {'Solukhumbu': 'dis-68'}, {'Sunsari': 'dis-69'}, {'Surkhet': 'dis-70'}, {'Syangja': 'dis-71'}, {'Tanahu': 'dis-72'}, {'Taplejung': 'dis-73'}, {'Terhathum': 'dis-74'}, {'Udayapur': 'dis-75'}, {'Nawalparasi_W': 'dis-76'}, {'Rukum_W': 'dis-77'}]

def convert_json(input_file, output_file):
    with open(input_file, 'r') as data_file:
        data = json.load(data_file)

        def build_wazimap_feature(feature):
            old_type = feature['type']
            old_geometry = feature['geometry']
            old_properties = feature['properties']

            def get_district_geoid(name):
                for item in district_rel:
                    if name in item.keys():
                        return str(item[name])

            code = str(old_properties['DDGN'])
            name = str(old_properties['FIRST_GaPa']).title()
            division = str(old_properties['FIRST_Type']).title()
            parent_name = str(old_properties['FIRST_DIST']).title()
            parent_code = get_district_geoid(str(old_properties['FIRST_DIST']).title())
            new_properties = {
                'code': '{}-{}'.format('loc', code),
                'name': name,
                'geoid': '{}-{}'.format('loc', code),
                'level': 'local',
                'division': division,
                'parent_name': parent_name,
                'parent_code': parent_code
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
    inputjson = ''
    outputjson = ''
    try:
        opts, args = getopt.getopt(args, 'hi:o:',
                                   ['inputjson=', 'outputjson='])
    except getopt.GetoptError:
        print('python set_local_geojson_properties.py -i <inputjson> -o <outputjson>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('python set_local_geo_properties.py '
                  '-i <inputjson> '
                  '-o <outputjson>')
            sys.exit()
        elif opt in ('-i', '--inputjson'):
            inputjson = arg
        elif opt in ('-o', '--outputjson'):
            outputjson = arg

    convert_json(inputjson, outputjson)


if __name__ == '__main__':
    main(sys.argv[1:])
