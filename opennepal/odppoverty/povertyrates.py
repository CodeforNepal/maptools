import csv
import getopt
from itertools import groupby
from operator import itemgetter
import os
import sys




names_to_geo_ids = {
    'Aachham': '68',
    'Achham': '68',
    'Arghakhanchi': '46',
    'Baglung': '51',
    'Baitadi': '73',
    'Bajhang': '69',
    'Bajura': '67',
    'Banke': '65',
    'Bara': '32',
    'Bardiya': '66',
    'Bhaktapur': '25',
    'Bhojpur': '06',
    'Chitwan': '35',
    'Chitawan': '35',
    'Dadeldhura': '74',
    'Dailekha': '63',
    'Dailekh': '63',
    'Dang': '60',
    'Darchaula': '72',
    'Darchula': '72',
    'Dhading': '30',
    'Dhankuta': '07',
    'Dhanusha': '20',
    'Dhanusa': '20',
    'Dolakha': '17',
    'Dolpa': '52',
    'Doti': '70',
    'Gorkha': '36',
    'Gulmi': '45',
    'Humla': '56',
    'Illam': '03',
    'Ilam': '03',
    'Jajarkot': '62',
    'Jhapa': '04',
    'Jumla': '54',
    'Kailali': '71',
    'Kalikot': '55',
    'Kanchanpur': '75',
    'Kapilbastu': '47',
    'Kaski': '40',
    'Kathmandu': '27',
    'Kavrepalanchowk': '24',
    'Kavrepalanchok': '24',
    'Kavre': '24',
    'Khotang': '13',
    'Lalitpur': '26',
    'Lamjung': '37',
    'Mahottari': '21',
    'Makawanpur': '34',
    'Makwanpur': '34',
    'Manang': '39',
    'Morang': '09',
    'Mugu': '53',
    'Mustang': '48',
    'Myagdi': '49',
    'Nawalparasi': '42',
    'Nuwakot': '29',
    'Okhaldhunga': '12',
    'Palpa': '43',
    'Panchthar': '02',
    'Parbat': '50',
    'Parsa': '33',
    'Pyuthan': '59',
    'Ramechhap': '18',
    'Rasuwa': '28',
    'Rautahat': '31',
    'Rolpa': '58',
    'Rukum': '57',
    'Rupandehi': '44',
    'Salyan': '61',
    'Sankhuwasabha': '05',
    'Saptari': '15',
    'Sarlahi': '22',
    'Sindhuli': '19',
    'Sindhupalchowk': '23',
    'Sindhupalchok': '23',
    'Siraha': '16',
    'Solukhumbu': '11',
    'Sunsari': '10',
    'Surkhet': '64',
    'Syangja': '41',
    'Tanahun': '38',
    'Tanahu': '38',
    'Taplejung': '01',
    'Tehrathum': '08',
    'Terhathum': '08',
    'Udayapur': '14',
}


def poverty_pop(percent_dict):
    geo_code = names_to_geo_ids[percent_dict['District']]
    total_pop = int(float(percent_dict['Population']))
    pov_percent = round(float(percent_dict['Poverty Incidence']), 5)
    in_poverty = int(total_pop * pov_percent)
    not_in_poverty = total_pop - in_poverty
    return [
        {'geo_level': 'district',
         'geo_code': geo_code,
         'poverty': 'IN_POVERTY',
         'total': in_poverty
         },
        {'geo_level': 'district',
         'geo_code': geo_code,
         'poverty': 'NOT_IN_POVERTY',
         'total': not_in_poverty
         }
    ]


def national_totals(district_rows):
    getter = itemgetter('poverty')
    return [{
                'geo_level': 'country',
                'geo_code': 'NP',
                'poverty': key,
                'total': sum(map(lambda i: i['total'], group))
            }
            for key, group in groupby(sorted(district_rows, key=getter),
                                      getter)]


def convert_csv(inputfile, outputfile):
    print('Input file: {}, \nOutput file: {}'.format(inputfile, outputfile))
    desired_keys = ['District', 'Indicators', 'Value']
    with open(inputfile, 'r') as data:
        reader = csv.DictReader(data)

        desired_rows = [{desired_key: row[desired_key] for desired_key
                         in desired_keys} for row in reader
                        if row['Year AD'] == '2011' and
                        (row['Indicators'] == 'Population' or
                         row['Indicators'] == 'Poverty Incidence')]

        desired_rows.sort(key=itemgetter('District'))

    blended_rows = []
    for key, group in groupby(desired_rows, lambda row: row['District']):
        pair = list(group)
        blended = {'District': key}
        for item in pair:
            blended[item['Indicators']] = item['Value']
        blended_rows.append(blended)

    district_rows = [item for sublist in list(map(poverty_pop, blended_rows))
                     for item in sublist]

    all_rows = district_rows + national_totals(district_rows)
    sorted_rows = sorted(all_rows, key=lambda x: (x.get('geo_code'),
                                                  x.get('poverty')))

    with open(outputfile, 'w') as csv_out:
        csv_keys = sorted_rows[0].keys()
        writer = csv.DictWriter(csv_out, fieldnames=csv_keys)
        writer.writeheader()
        for row in sorted_rows:
            writer.writerow(row)


def main(args):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(args, 'hi:o:',
                                   ['inputfile=', 'outputfile='])
    except getopt.GetoptError:
        print('python povertyrates.py -i <inputfile> -o <outputfile> ')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('python povertyrates.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ('-i', '--inputfile'):
            inputfile = arg
        elif opt in ('-o', '--outputfile'):
            outputfile = arg

    convert_csv(inputfile, outputfile)

    print('Done!')

if __name__ == '__main__':
    main(sys.argv[1:])
