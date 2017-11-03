import csv
import getopt

import sys
from collections import namedtuple

from shared import geoidmappings

'''
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
    'Chitwa': '35',
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
    'Kapilavastu': '47',
    'Kapilvastu': '47',
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
    'Nawalparashi': '42',
    'Nuwakot': '29',
    'Okhaldhunga': '12',
    'OKhaldhunga': '12',
    'Palpa': '43',
    'Panchthar': '02',
    'Parbat': '50',
    'Parsa': '33',
    'Pyuthan': '59',
    'Ramechap': '18',
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
    'Tahanun': '38',
    'Taplejung': '01',
    'Tehrathum': '08',
    'Terhathum': '08',
    'Terathum': '08',
    'Udayapur': '14',
    'Udaypur': '14'
}
'''

meat_types = [
    'buff', 
    'mutton',
    'chevon',
    'pork',
    'chicken',
    'duck',
    'total'
]

COLUMNS = {
    'district_code': 0,
    'district_name': 0,
    'buff': 1,
    'mutton': 2,
    'chevon': 3,
    'pork': 4,
    'chicken': 5,
    'duck': 6,
    'total': 7
}

ConvertedRow = namedtuple('ConvertedRow', 
    ['district_code', 
     'district_name'
    ] +
    meat_types
)

def national_totals(district_rows):
    group = [row for row in district_rows]

    # find any missing districts
    all_districts = set([val for _, val 
        in geoidmappings.names_to_geo_ids.iteritems()])

    districts_with_data = set([row['geo_code'] for row 
        in district_rows])

    print(all_districts - districts_with_data)
    #return list(all_districts - districts_with_data) + [{
    return [{
            'geo_level': 'country',
            'geo_code': 'NP',
            'buff': sum(map(lambda i: int(i['buff']), group)),
            'mutton': sum(map(lambda i: int(i['mutton']), group)),
            'chevon': sum(map(lambda i: int(i['chevon']), group)),
            'pork': sum(map(lambda i: int(i['pork']), group)),
            'chicken': sum(map(lambda i: int(i['chicken']), group)),
            'duck': sum(map(lambda i: int(i['duck']), group)),
            'total': sum(map(lambda i: int(i['total']), group))
    }]

def deaths_for_district(death_row_tuple):
    geo_level = 'district'
    name_title = death_row_tuple.district_name.title()
    if name_title not in geoidmappings.names_to_geo_ids:
        print('Unknown district:{0}'.format(
            name_title)
        )
        return []

    geo_code = geoidmappings.names_to_geo_ids[
        death_row_tuple.district_name.title().strip('\n')]
    return [
        {
            'geo_code': geo_code,
            'geo_level': geo_level,
            'buff': death_row_tuple.buff,
            'mutton': death_row_tuple.mutton,
            'chevon': death_row_tuple.chevon,
            'pork': death_row_tuple.pork,
            'chicken': death_row_tuple.chicken,
            'duck': death_row_tuple.duck,
            'total': death_row_tuple.total
        }
    ]

def get_cell_number(cell):
    return cell if cell else '0'

def convert_csv(inputfile, outputfile):
    print('Input file: {}\nOutput file: {}'.format(inputfile, outputfile))
    with open(inputfile, 'r') as data, open(outputfile, 'w') as csv_out:
        reader = csv.reader(data)
        csv_rows = [row for row in reader][1:]
        
        district_data = [row for district_deliveries
                         in
                         [deaths_for_district(
                             ConvertedRow(row[COLUMNS['district_code']],
                                         row[COLUMNS['district_name']],
                                         get_cell_number(row[COLUMNS['buff']]),
                                         get_cell_number(row[COLUMNS['mutton']]),
                                         get_cell_number(row[COLUMNS['chevon']]),
                                         get_cell_number(row[COLUMNS['pork']]),
                                         get_cell_number(row[COLUMNS['chicken']]),
                                         get_cell_number(row[COLUMNS['duck']]),
                                         get_cell_number(row[COLUMNS['total']])))
                             for row in csv_rows if
                             row[COLUMNS['district_code']]]
                         for row in district_deliveries]

        csv_keys = ['geo_code', 'geo_level', 'meat', 'total']
        writer = csv.writer(csv_out)
        writer.writerow(csv_keys)
        for row in national_totals(district_data) + district_data:
            for meattype in ['buff', 'mutton', 'chevon', 'pork', 'chicken', 'duck']:
                writer.writerow([row['geo_code'], row['geo_level'], 
                    meattype.upper(), row[meattype]])
            writer.writerow([row['geo_code'], row['geo_level'], 
               'TOTAL', row['total']])


def main(args):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(args, 'hi:o:',
                                   ['inputfile=',
                                    'outputfile='])
    except getopt.GetoptError:
        print('python deliveries.py '
              '-i <inputfile> '
              '-o <outputfile> ')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('python deliveries.py '
                  '-i <inputfile> '
                  '-o <outputfile> ')
            sys.exit()
        elif opt in ('-i', '--inputfile'):
            inputfile = arg
        elif opt in ('-o', '--outputfile'):
            outputfile = arg

    convert_csv(inputfile, outputfile)

    print('Done!')


if __name__ == '__main__':
    main(sys.argv[1:])
