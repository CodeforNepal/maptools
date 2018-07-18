import getopt
import csv
import json
import re
import sys


'''
Script to grab basic details about each district from the district.geojson file
and build a CSV for analysis of names and parent to which each district is assigned
'''

names_to_geo_ids = [{'Jhapa': 1}, {'Ilam': 1}, {'Panchthar': 1}, {'Taplejung': 1}, {'Morang': 1}, {'Sunsari': 1}, {'Bhojpur': 1}, {'Dhankuta': 1}, {'Tehrathum': 1}, {'Sankhuwasabha': 1}, {'Saptari': 2}, {'Siraha': 2}, {'Udayapur': 1}, {'Khotang': 1}, {'Okhaldhunga': 1}, {'Solukhumbu': 1}, {'Dhanusa': 2}, {'Mahottari': 2}, {'Sarlahi': 2}, {'Sindhuli': 3}, {'Ramechhap': 3}, {'Dolakha': 3}, {'Bhaktapur': 3}, {'Dhading': 3}, {'Kathmandu': 3}, {'Kavrepalanchowk': 3}, {'Lalitpur': 3}, {'Nuwakot': 3}, {'Rasuwa': 3}, {'Sindhupalchok': 3}, {'Bara': 2}, {'Parsa': 2}, {'Rautahat': 2}, {'Chitwan': 3}, {'Makwanpur': 3}, {'Gorkha': 4}, {'Kaski': 4}, {'Lamjung': 4}, {'Syangja': 4}, {'Tanahu': 4}, {'Manang': 4}, {'Kapilvastu': 5}, {'Nawalpur': 4}, {'Parasi': 5}, {'Rupandehi': 5}, {'Arghakhanchi': 5}, {'Gulmi': 5}, {'Palpa': 5}, {'Baglung': 4}, {'Myagdi': 4}, {'Parbat': 4}, {'Mustang': 4}, {'Dang': 5}, {'Pyuthan': 5}, {'Rolpa': 5}, {'Eastern Rukum': 5}, {'Western Rukum': 6}, {'Salyan': 6}, {'Dolpa': 6}, {'Humla': 6}, {'Jumla': 6}, {'Kalikot': 6}, {'Mugu': 6}, {'Banke': 5}, {'Bardiya': 5}, {'Surkhet': 6}, {'Dailekh': 6}, {'Jajarkot': 6}, {'Kailali': 7}, {'Achham': 7}, {'Doti': 7}, {'Bajhang': 7}, {'Bajura': 7}, {'Kanchanpur': 7}, {'Dadeldhura': 7}, {'Baitadi': 7}, {'Darchula': 7}]

def convert_csv(input_file, output_file):
    with open(input_file, 'r') as data_file:
        data = json.load(data_file)

        def select_keys_from_properties(district):

            def get_parent_geoid(name):
                for item in names_to_geo_ids:
                    # import pdb
                    # pdb.set_trace()

                    if name[0] in item.keys():
                        return item[name[0]]
            
            
            print(district['name'])
            return {
                'name': district['name'],
                'geocode': district['code'],
                'year': '2016',
                'parent_level': 'province',
                'long_name': district['name'],
                'geo_level': 'district',
                'parent_code': get_parent_geoid([district['name']])
            }

        properties = list(map(lambda f: select_keys_from_properties(
            f['properties']), data['features']))

        # print(properties)
        # print("Count: ", len(properties))

        # import pdb
        # pdb.set_trace()
        
        fieldnames = ['name', 'geocode', 'year', 'parent_level', 'long_name', 'geo_level', 'parent_code']

        sorted_properties = sorted(properties, key=lambda elem: "%s" % (elem['geocode']))

        with open(output_file, 'w') as csv_out:
            writer = csv.DictWriter(csv_out, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sorted_properties)

    print('Done!')


def main(args):
    inputjson = ''
    outputcsv = ''
    try:
        opts, args = getopt.getopt(args, 'hi:o:',
                                   ['inputjson=', 'outputcsv='])
    except getopt.GetoptError:
        print('python district_geojson_to_csv.py -i <inputjson> -o <outputcsv>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('python district_geojson_to_csv.py -i <inputjson> -o <outputcsv>')
            sys.exit()
        elif opt in ('-i', '--inputjson'):
            inputjson = arg
        elif opt in ('-o', '--outputcsv'):
            outputcsv = arg

    convert_csv(inputjson, outputcsv)


if __name__ == '__main__':
    main(sys.argv[1:])
