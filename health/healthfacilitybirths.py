import csv
import getopt

import sys
from collections import namedtuple

from shared import geoidmappings


FacilityBirthsPercent = namedtuple('FacilityBirthsPercent', ['location',
                                                             'percent'])


def facility_births(births_tuple):
    if births_tuple.location == 'National Total':
        geo_level = 'country'
        geo_code = 'NP'
    else:
        geo_level = 'district'
        geo_code = geoidmappings.names_to_geo_ids[
            births_tuple.location.title()]
    return {
        'geo_level': geo_level,
        'geo_code': geo_code,
        'health_facility_births_percent':
            "{value:.{digits}f}".format(value=float(births_tuple.percent),
                                         digits=2)
            if births_tuple.percent else 0.0
    }



def convert_csv(inputfile, outputfile):
    print('Input file: {}\nOutput file: {}'.format(inputfile, outputfile))
    with open(inputfile, 'r') as data, open(outputfile, 'w') as csv_out:
        reader = csv.reader(data)
        csv_rows = [row for row in reader][1:]
        parties_data = [facility_births(FacilityBirthsPercent(row[1], row[2]))
                        for row in csv_rows
                        if row[0] or row[1] == 'National Total']
        csv_keys = ['geo_level', 'geo_code', 'health_facility_births_percent']
        writer = csv.writer(csv_out)
        writer.writerow(csv_keys)
        for row in parties_data:
            writer.writerow([row['geo_level'],
                            row['geo_code'],
                            row['health_facility_births_percent']])


def main(args):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(args, 'hi:o:',
                                   ['inputfile=',
                                    'outputfile='])
    except getopt.GetoptError:
        print('python healthfacilitybirths.py '
              '-i <inputfile> -o <outputfile> ')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('python healthfacilitybirths.py '
                  '-i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ('-i', '--inputfile'):
            inputfile = arg
        elif opt in ('-o', '--outputfile'):
            outputfile = arg

    convert_csv(inputfile, outputfile)

    print('Done!')


if __name__ == '__main__':
    main(sys.argv[1:])
