import getopt
import csv
import json
import sys


'''
Script to grab basic details about each VDC from the vdc.geojson file
and build a CSV for analysis of names and districts to which each VDC is
assigned
'''

names_to_geo_ids = {
    'Khotang': '13',
    'Rautahat': '31',
    'Dailekh': '63',
    'Ramechhap': '18',
    'Banke': '65',
    'Sarlahi': '22',
    'Myagdi': '49',
    'Sindhuli': '19',
    'Gulmi': '45',
    'Saptari': '15',
    'Parsa': '33',
    'Rasuwa': '28',
    'Salyan': '61',
    'Rupandehi': '44',
    'Mugu': '53',
    'Bajura': '67',
    'Dhankuta': '07',
    'Dang': '60',
    'Kathmandu': '27',
    'Sankhuwasabha': '05',
    'Solukhumbu': '11',
    'Doti': '70',
    'Arghakhanchi': '46',
    'Baglung': '51',
    'Bhojpur': '06',
    'Dhanusha': '20',
    'Dhanusa': '20',
    'Panchthar': '02',
    'Kalikot': '55',
    'Tahanun': '38',
    'Tanahu': '38',
    'Bardiya': '66',
    'Lalitpur': '26',
    'Humla': '56',
    'Kaski': '40',
    'Syangja': '41',
    'Dadeldhura': '74',
    'Dhading': '30',
    'Pyuthan': '59',
    'Taplejung': '01',
    'Rolpa': '58',
    'Bhaktapur': '25',
    'Lamjung': '37',
    'Sunsari': '10',
    'Kapilbastu': '47',
    'Kanchanpur': '75',
    'Kailali': '71',
    'Sindhupalchowk': '23',
    'Sindhupalchok': '23',
    'Jumla': '54',
    'Morang': '09',
    'Dolpa': '52',
    'Surkhet': '64',
    'Siraha': '16',
    'Nawalparasi': '42',
    'Chitwan': '35',
    'Chitawan': '35',
    'Jhapa': '04',
    'Baitadi': '73',
    'Achham': '68',
    'Makawanpur': '34',
    'Makwanpur': '34',
    'Bara': '32',
    'Okhaldhunga': '12',
    'Rukum': '57',
    'Darchula': '72',
    'Tehrathum': '08',
    'Terhathum': '08',
    'Nuwakot': '29',
    'Bajhang': '69',
    'Mustang': '48',
    'Parbat': '50',
    'Udayapur': '14',
    'Illam': '03',
    'Ilam': '03',
    'Manang': '39',
    'Palpa': '43',
    'Dolakha': '17',
    'Jajarkot': '62',
    'Mahottari': '21',
    'Kavre': '24',
    'Kavrepalanchok': '24',
    'Gorkha': '36'
}


def convert_csv(input_file, output_file):
    with open(input_file, 'r') as data_file:
        data = json.load(data_file)

        def select_keys_from_vdc_properties(vdc):
            district_name = vdc['NAME_3']
            district_id = names_to_geo_ids[district_name]
            return {
                'country': vdc['NAME_0'],
                'region': vdc['NAME_1'],
                'zone': vdc['NAME_2'],
                'district_id': district_id,
                'district': district_name,
                'vdc': vdc['NAME_4'],

            }
        properties = list(map(lambda f: select_keys_from_vdc_properties(
            f['properties']), data['features']))
        len(properties)
        
        fieldnames = ['country', 'region', 'zone', 'district_id', 'district',
                      'vdc']

        sorted_properties = sorted(properties, key=lambda
            elem: "%s %s %s %s" %
                  (elem['region'], elem['zone'], elem['district_id'],
                   elem['vdc']))

        with open(output_file, 'w') as csv_out:
            writer = csv.DictWriter(csv_out, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sorted_properties)

    print('Done!')


def main(args):
    indir = ''
    outputcsv = ''
    try:
        opts, args = getopt.getopt(args, 'hi:o:',
                                   ['indir=', 'outputcsv='])
    except getopt.GetoptError:
        print('python vdc_to_csv.py -i <indir> -o <outputcsv>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('python vdc_to_csv.py -i <indir> -o <outputcsv>')
            sys.exit()
        elif opt in ('-i', '--indir'):
            indir = arg
        elif opt in ('-o', '--outputcsv'):
            outputcsv = arg

    convert_csv(indir, outputcsv)


if __name__ == '__main__':
    main(sys.argv[1:])
