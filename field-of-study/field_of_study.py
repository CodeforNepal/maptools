import csv
import getopt
import sys
from itertools import groupby
from operator import itemgetter

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


def normalize(input_file, output_file):
    with open(input_file, 'r') as data_in, open(output_file, 'w') as data_out:
        reader = csv.reader(data_in)
        writer = csv.writer(data_out)
        first = next(reader)
        fields = list((filter(lambda f: len(f) > 0, first)))
        column_headers = list(map(lambda c: c.upper().replace(' ', '_')
                                  .replace(',', ''), fields)) + ['NOT_STATED']
        male_headers = list(map(lambda h: h + '_MALE', column_headers))
        female_headers = list(map(lambda h: h + '_FEMALE', column_headers))
        joined_headers = [val for pair in zip(male_headers, female_headers) for
                          val in pair]
        writer.writerow(['DISTRICT'] + joined_headers)
        more = True
        district_rows = []
        while more:
            try:
                district_name_row = next(reader)
                if district_name_row \
                        and district_name_row[0] \
                        and len(district_name_row[0]) > 0:
                    more = True
                    district_name = district_name_row[0]
                    next(reader)  # consumed but not used
                    male_row = next(reader)
                    female_row = next(reader)
                    counts = [val for pair in zip(male_row[1:], female_row[1:])
                              for val in pair]
                    district_rows.append([district_name] + counts)
                else:
                    more = False
            except StopIteration:
                more = False
        for row in sorted(district_rows, key=lambda r: r[0]):
            writer.writerow(row)

    return output_file


def national_totals(district_rows):
    totals = []
    getter = itemgetter('field of study', 'sex')
    for key, group in groupby(sorted(district_rows, key=getter), getter):
        totals.append(
            {
                'geo_level': 'country',
                'geo_code': 'NP',
                'field of study': key[0],
                'sex': key[1],
                'total': sum(map(lambda i: i['total'], group))
            }
        )

    return totals


def extract_sex_from_value_name(value_name):
    if value_name.endswith('_MALE'):
        sex = 'male'
    elif value_name.endswith('_FEMALE'):
        sex = 'female'
    else:
        sex = None
    name = value_name.replace('_FEMALE', '').replace('_MALE', '')
    return name, sex


def convert_csv(input_file, output_file):
    district_rows = []
    with open(input_file, 'r') as data:
        reader = csv.DictReader(data)
        for row in reader:
            geo_code = names_to_geo_ids[row['DISTRICT']]
            row.pop('DISTRICT', None)
            for key, total in row.items():
                field_of_study, sex = extract_sex_from_value_name(key)
                if sex in ['male', 'female']:
                    data_row = {
                        'geo_level': 'district',
                        'geo_code': geo_code,
                        'field of study': field_of_study,
                        'sex': sex,
                        'total': int(total)
                    }
                    district_rows.append(data_row)

    all_rows = district_rows + national_totals(district_rows)
    sorted_rows = sorted(all_rows, key=lambda x: (x.get('geo_code'),
                                                  x.get('field of study'),
                                                  x.get('sex')))
    with open(output_file, 'w') as csv_out:
        csv_keys = sorted_rows[0].keys()
        writer = csv.DictWriter(csv_out, fieldnames=csv_keys)
        writer.writeheader()
        for row in sorted_rows:
            writer.writerow(row)


def main(args):
    inputcsv = ''
    intermediatecsv = ''
    finalcsv = ''
    try:
        opts, args = getopt.getopt(args, 'hi:o:f:',
                                   ['inputcsv=', 'intermediatecsv=',
                                    'finalcsv='])
    except getopt.GetoptError:
        print('python field_of_study.py -i <inputcsv> -o <intermediatecsv> '
              '-f ,<finalcsv>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('python field_of_study.py -i <inputcsv> '
                  '-o <intermediatecsv> -f ,<finalcsv>')
            sys.exit()
        elif opt in ('-i', '--inputcsv'):
            inputcsv = arg
        elif opt in ('-o', '--intermediatecsv'):
            intermediatecsv = arg
        elif opt in ('-f', '--finalcsv'):
            finalcsv = arg
    file_to_convert = normalize(inputcsv, intermediatecsv)

    convert_csv(file_to_convert, finalcsv)

    print('Done!')


if __name__ == '__main__':
    main(sys.argv[1:])
