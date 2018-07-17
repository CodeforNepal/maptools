import getopt
import csv
import json
import re
import sys


'''
Script to grab basic details about each district from the district.geojson file
and build a CSV for analysis of names and parent to which each district is assigned
'''

names_to_geo_ids = [{'Nawalparasi': '3585'}, {'Rupandehi': '3703'}, {'Jhapa': '1581'}, {'Ilam': '1538'}, {'Panchthar': '1658'}, {'Taplejung': '1658'}, {'Morang': '1326'}, {'Sunsari': '1467'}, {'Bhojpur': '1236'}, {'Dhankuta': '1299'}, {'Terathum': '1475'}, {'Sankhuwasabha': '1394'}, {'Saptari': '1910'}, {'Siraha': '2001'}, {'Udayapur': '2123'}, {'Khotang': '1709'}, {'Okhaldhunga': '1809'}, {'Solukhumbu': '2050'}, {'Dhanusa': '496'}, {'Mahottari': '614'}, {'Sarlahi': '763'}, {'Sindhuli': '829'}, {'Ramechhap': '650'}, {'Dolakha': '528'}, {'Bhaktapur': '2'}, {'Dhading': '51'}, {'Kathmandu': '100'}, {'Kavrepalanchok': '190'}, {'Lalitpur': '244'}, {'Nuwakot': '268'}, {'Rasuwa': '319'}, {'Sindhupalchowk': '81'}, {'Parsa': '1101'}, {'Rautahat': '1123'}, {'Chitwan': '953'}, {'Makwanpur': '1006'}, {'Gorkha': '3077'}, {'Kaski': '3111'}, {'Lamjung': '3190'}, {'Syangja': '3227'}, {'Tanahun': '3324'}, {'Manag': '3212'}, {'Kapilbastu': '3487'}, {'Nawalparasi': '3579'}, {'Rupandehi': '3715'}, {'Arghakhanchi': '3357'}, {'Gulmi': '3427'}, {'Palpa': '3630'}, {'Baglung': '2890'}, {'Myagdi': '2972'}, {'Parbat': '3020'}, {'Mustang': '2920'}, {'Dang': '2671'}, {'Pyuthan': '2714'}, {'Banke': '2530'}, {'Bardiya': '2593'}, {'Mugu': '3746'}, {'Dolpa': '3751'}, {'Kanchanpur': '2269'}, {'Dadeldhura': '2192'}, {'Baitadi': '2132'}, {'Bajhang': '2349'}, {'Darchula': '2221'}, {'Jumla': '3759'}, {'Humla': '3738'}, {'Kailali': '2503'}, {'Surkhet': '2618'}, {'Doti': '2440'}, {'Kalikot': '3768'}, {'Bajura': '2407'}, {'Achham': '2329'}, {'Jajarkot': '3783'}, {'Dailekh': '3792'}, {'Rukum': '2807'}, {'Salyan': '2856'}, {'Rolpa': '2785'}, {'Bara': 'None'}]

def convert_csv(input_file, output_file):
    with open(input_file, 'r') as data_file:
        data = json.load(data_file)

        def select_keys_from_properties(local):

            def get_parent_geoid(name):
                for item in names_to_geo_ids:
                    if name[0] in item.keys():
                        return item[name[0]]
            
            
            return {
                'name': local['name'],
                'geocode': local['code'],
                'year': '2016',
                'parent_level': 'district',
                'long_name': local['name'],
                'geo_level': 'local',
                'parent_code': get_parent_geoid([local['parent']])
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
        print('python local_geojson_to_csv.py -i <inputjson> -o <outputcsv>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('python local_geojson_to_csv.py -i <inputjson> -o <outputcsv>')
            sys.exit()
        elif opt in ('-i', '--inputjson'):
            inputjson = arg
        elif opt in ('-o', '--outputcsv'):
            outputcsv = arg

    convert_csv(inputjson, outputcsv)


if __name__ == '__main__':
    main(sys.argv[1:])
