import csv
import getopt
from shared import geoidmappings
import sys


def convert_csv(input_file, output_file, column, separator):
    rows = []
    with open(input_file, 'r') as data:
        reader = csv.DictReader(data, delimiter=separator)
        for row in reader:
            geo_code = geoidmappings.names_to_geo_ids[row['district']]
            rows.append({
                'geo_level': 'district',
                'geo_code': geo_code,
                column: row[column].replace(',', '')
            })
    sorted_rows = sorted(rows, key=lambda x: x.get('geo_code'))
    with open(output_file, 'w') as csv_out:
        csv_keys = sorted_rows[0].keys()
        writer = csv.DictWriter(csv_out, fieldnames=csv_keys)
        writer.writeheader()
        for row in sorted_rows:
            writer.writerow(row)

    print('Done!')


def main(args):
    indir = ''
    outputcsv = ''
    column = ''
    separator = ','
    try:
        opts, args = getopt.getopt(args, 'hi:o:c:t',
                                   ['indir=', 'outputcsv=',
                                    'column=', 'tabseparated'])
    except getopt.GetoptError:
        print('python singlefield.py -i <indir> -o <outputcsv> '
              '-c <column> -t')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('python singlefield.py -i <indir> -o <outputcsv> '
                  '-c <column> -t')
            sys.exit()
        elif opt in ('-i', '--indir'):
            indir = arg
        elif opt in ('-o', '--outputcsv'):
            outputcsv = arg
        elif opt in ('-c', '--column'):
            column = arg
        elif opt in ('-t', '--tabseparated'):
            separator = '\t'

    convert_csv(indir, outputcsv, column, separator)

if __name__ == '__main__':
    main(sys.argv[1:])
