import getopt
import csv
import json
import re
import sys


'''
Script to grab basic details about each district from the district.geojson file
and build a CSV for analysis of names and parent to which each district is assigned
'''

names_to_geo_ids = [{'Jhapa': 'pro-1'}, {'Ilam': 'pro-1'}, {'Panchthar': 'pro-1'}, {'Taplejung': 'pro-1'}, {'Morang': 'pro-1'}, {'Sunsari': 'pro-1'}, {'Bhojpur': 'pro-1'}, {'Dhankuta': 'pro-1'}, {'Tehrathum': 'pro-1'}, {'Sankhuwasabha': 'pro-1'}, {'Saptari': 'pro-2'}, {'Siraha': 'pro-2'}, {'Udayapur': 'pro-1'}, {'Khotang': 'pro-1'}, {'Okhaldhunga': 'pro-1'}, {'Solukhumbu': 'pro-1'}, {'Dhanusa': 'pro-2'}, {'Mahottari': 'pro-2'}, {'Sarlahi': 'pro-2'}, {'Sindhuli': 'pro-3'}, {'Ramechhap': 'pro-3'}, {'Dolakha': 'pro-3'}, {'Bhaktapur': 'pro-3'}, {'Dhading': 'pro-3'}, {'Kathmandu': 'pro-3'}, {'Kavrepalanchowk': 'pro-3'}, {'Lalitpur': 'pro-3'}, {'Nuwakot': 'pro-3'}, {'Rasuwa': 'pro-3'}, {'Sindhupalchowk': 'pro-3'}, {'Bara': 'pro-2'}, {'Parsa': 'pro-2'}, {'Rautahat': 'pro-2'}, {'Chitwan': 'pro-3'}, {'Makwanpur': 'pro-3'}, {'Gorkha': 'pro-4'}, {'Kaski': 'pro-4'}, {'Lamjung': 'pro-4'}, {'Syangja': 'pro-4'}, {'Tanahu': 'pro-4'}, {'Manang': 'pro-4'}, {'Kapilvastu': 'pro-5'}, {'Nawalpur': 'pro-4'}, {'Parasi': 'pro-5'}, {'Rupandehi': 'pro-5'}, {'Arghakhanchi': 'pro-5'}, {'Gulmi': 'pro-5'}, {'Palpa': 'pro-5'}, {'Baglung': 'pro-4'}, {'Myagdi': 'pro-4'}, {'Parbat': 'pro-4'}, {'Mustang': 'pro-4'}, {'Dang': 'pro-5'}, {'Pyuthan': 'pro-5'}, {'Rolpa': 'pro-5'}, {'Eastern Rukum': 'pro-5'}, {'Nawalparasi': 'pro-5'}, {'Salyan': 'pro-6'}, {'Dolpa': 'pro-6'}, {'Humla': 'pro-6'}, {'Jumla': 'pro-6'}, {'Kalikot': 'pro-6'}, {'Mugu': 'pro-6'}, {'Banke': 'pro-5'}, {'Bardiya': 'pro-5'}, {'Surkhet': 'pro-6'}, {'Dailekh': 'pro-6'}, {'Jajarkot': 'pro-6'}, {'Kailali': 'pro-7'}, {'Achham': 'pro-7'}, {'Doti': 'pro-7'}, {'Bajhang': 'pro-7'}, {'Bajura': 'pro-7'}, {'Kanchanpur': 'pro-7'}, {'Dadeldhura': 'pro-7'}, {'Baitadi': 'pro-7'}, {'Darchula': 'pro-7'}]

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
                'geocode': 'dis-'+str(district['code']),
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
