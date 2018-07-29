import getopt
import csv
import json
import re
import sys


'''
Script to grab basic details about each district from the district.geojson file
and build a CSV for analysis of names and parent to which each district is assigned
'''

names_to_geo_ids = [{'Nawalparasi': 'dis-3585'}, {'Rupandehi': 'dis-3703'}, {'Jhapa': 'dis-1581'}, {'Ilam': 'dis-1538'}, {'Panchthar': 'dis-1658'}, {'Taplejung': 'dis-1659'}, {'Morang': 'dis-1326'}, {'Sunsari': 'dis-1467'}, {'Bhojpur': 'dis-1236'}, {'Dhankuta': 'dis-1299'}, {'Terathum': 'dis-1475'}, {'Sankhuwasabha': 'dis-1394'}, {'Saptari': 'dis-1910'}, {'Siraha': 'dis-2001'}, {'Udayapur': 'dis-2123'}, {'Khotang': 'dis-1709'}, {'Okhaldhunga': 'dis-1809'}, {'Solukhumbu': 'dis-2050'}, {'Dhanusa': 'dis-496'}, {'Mahottari': 'dis-614'}, {'Sarlahi': 'dis-763'}, {'Sindhuli': 'dis-829'}, {'Ramechhap': 'dis-650'}, {'Dolakha': 'dis-528'}, {'Bhaktapur': 'dis-2'}, {'Dhading': 'dis-51'}, {'Kathmandu': 'dis-100'}, {'Kavrepalanchok': 'dis-190'}, {'Lalitpur': 'dis-244'}, {'Nuwakot': 'dis-268'}, {'Rasuwa': 'dis-319'}, {'Sindhupalchowk': 'dis-81'}, {'Parsa': 'dis-1101'}, {'Rautahat': 'dis-1123'}, {'Chitwan': 'dis-953'}, {'Makwanpur': 'dis-1006'}, {'Gorkha': 'dis-3077'}, {'Kaski': 'dis-3111'}, {'Lamjung': 'dis-3190'}, {'Syangja': 'dis-3227'}, {'Tanahun': 'dis-3324'}, {'Manag': 'dis-3212'}, {'Kapilbastu': 'dis-3487'}, {'Nawalparasi': 'dis-3579'}, {'Rupandehi': 'dis-3715'}, {'Arghakhanchi': 'dis-3357'}, {'Gulmi': 'dis-3427'}, {'Palpa': 'dis-3630'}, {'Baglung': 'dis-2890'}, {'Myagdi': 'dis-2972'}, {'Parbat': 'dis-3020'}, {'Mustang': 'dis-2920'}, {'Dang': 'dis-2671'}, {'Pyuthan': 'dis-2714'}, {'Banke': 'dis-2530'}, {'Bardiya': 'dis-2593'}, {'Mugu': 'dis-3746'}, {'Dolpa': 'dis-3751'}, {'Kanchanpur': 'dis-2269'}, {'Dadeldhura': 'dis-2192'}, {'Baitadi': 'dis-2132'}, {'Bajhang': 'dis-2349'}, {'Darchula': 'dis-2221'}, {'Jumla': 'dis-3759'}, {'Humla': 'dis-3738'}, {'Kailali': 'dis-2503'}, {'Surkhet': 'dis-2618'}, {'Doti': 'dis-2440'}, {'Kalikot': 'dis-3768'}, {'Bajura': 'dis-2407'}, {'Achham': 'dis-2329'}, {'Jajarkot': 'dis-3783'}, {'Dailekh': 'dis-3792'}, {'Rukum': 'dis-2807'}, {'Salyan': 'dis-2856'}, {'Rolpa': 'dis-2785'}, {'Bara': 'dis-5555'}]

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
                'geocode': 'loc-'+str(local['code']),
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
