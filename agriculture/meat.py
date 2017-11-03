import csv
import getopt
import sys
from collections import namedtuple

from shared import geoidmappings


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

    if len(all_districts - districts_with_data):
        print('Districts without data:{0}'.format(
            all_districts - districts_with_data)
        )

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
