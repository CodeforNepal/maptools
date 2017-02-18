import csv
import getopt
from itertools import groupby
from operator import itemgetter
from shared import geoidmappings
import sys


def langs_for_district(district_langs_tuple):
    '''
    :param district_langs_tuple: a tuple of [0] district and [1] a dict of
    language to total speakers of that language in the district. Ex:
    ('Banke', {'Avadhi': 116477, 'Nepali': 194238, 'Magar': 4644})
    :return: a list of dicts that matches the format needed for NepalMap
    '''
    return [{'geo_level': 'district',
             'geo_code': geoidmappings.names_to_geo_ids[
                 district_langs_tuple[0]],
             'language': language,
             'total': value
             } for (language, value) in district_langs_tuple[1]]


def national_totals(rows):
    '''
    :param rows: data from CSV to be transformed into dicts for NepalMap
    :return: a list of dicts for each of the languages spoken in Nepal
    '''
    lang_getter = itemgetter('Caste')
    rows.sort(key=lang_getter)
    national_langs = []
    for key, group in groupby(sorted(rows, key=lang_getter),
                              lang_getter):
        national_langs.append({
            'geo_level': 'country',
            'geo_code': 'NP',
            'language': key,
            'total': sum(map(
                lambda lang: int(lang['Value']) if lang['Value'] else 0,
                group))
        })
    return national_langs


def add_missing_langs_for_area(all_langs, lang_tuples_for_area):
    langs_not_in_area = set(all_langs) - set(map(lambda tup: tup[0],
                                                 lang_tuples_for_area))
    return [(lang, 0) for lang in langs_not_in_area]


def district_totals(rows):
    '''
    :param rows: data from CSV to be transformed into dicts for NepalMap
    :return: for each district, a dict for each of the languages spoken in
    Nepal. Any language not represented in the district is assigned a total
    of zero for the district.
    '''
    all_langs = set(map(lambda row: row['Caste'], rows))
    district_lang_getter = itemgetter('District', 'Caste')
    districts_dict = {}
    for key, group in groupby(sorted(rows, key=district_lang_getter),
                              district_lang_getter):
        district = key[0]
        language = key[1]
        speakers = sum(map(lambda i: int(i['Value']), group))

        if district not in districts_dict:
            districts_dict[district] = {}
        districts_dict[district][language] = speakers

    district_lang_data = []
    for district in districts_dict:
        lang_tuples = sorted(districts_dict[district].items(),
                              key=itemgetter(1), reverse=True)
        lang_totals_for_district = [lang for lang in lang_tuples]
        langs_not_in_district = add_missing_langs_for_area(
            all_langs, lang_totals_for_district)
        district_lang_data.append((district, lang_totals_for_district +
                                   langs_not_in_district))

    return [item for sublist in
            list(map(langs_for_district, district_lang_data)) for
            item in sublist]


def convert_csv(inputfile, outputfile):
    print('Input file: {}\nOutput file: {}'.format(inputfile, outputfile))
    desired_keys = ['District', 'Caste', 'Indicator', 'Value']
    with open(inputfile, 'r') as data:
        reader = csv.DictReader(data)

        rows = [{desired_key: row[desired_key] for desired_key
                 in desired_keys} for row in reader]

        national_langs = national_totals(rows)
        district_langs = district_totals(rows)

        all_langs = sorted(national_langs + district_langs,
                           key=lambda r: '{}{}{}'.
                           format(r['geo_level'], r['geo_code'], r['total']))

    with open(outputfile, 'w') as csv_out:
        csv_keys = all_langs[0].keys()
        writer = csv.DictWriter(csv_out, fieldnames=csv_keys)
        writer.writeheader()
        for row in all_langs:
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
