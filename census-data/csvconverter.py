from abc import ABCMeta, abstractmethod
import csv
import getopt
from itertools import groupby
from operator import itemgetter
import os
import sys


names_to_geo_ids = {
    'Khotang': '13', 'Rautahat': '31', 'Dailekh': '63',
    'Ramechhap': '18', 'Banke': '65', 'Sarlahi': '22',
    'Myagdi': '49', 'Sindhuli': '19', 'Gulmi': '45',
    'Saptari': '15', 'Parsa': '33', 'Rasuwa': '28',
    'Salyan': '61', 'Rupandehi': '44', 'Mugu': '53',
    'Bajura': '67', 'Dhankuta': '07', 'Dang': '60',
    'Kathmandu': '27', 'Sankhuwasabha': '05',
    'Solukhumbu': '11', 'Doti': '70',
    'Arghakhanchi': '46', 'Baglung': '51',
    'Bhojpur': '06', 'Dhanusha': '20', 'Panchthar': '02',
    'Kalikot': '55', 'Tahanun': '38', 'Bardiya': '66',
    'Lalitpur': '26', 'Humla': '56', 'Kaski': '40',
    'Syangja': '41', 'Dadeldhura': '74', 'Dhading': '30',
    'Pyuthan': '59', 'Taplejung': '01', 'Rolpa': '58',
    'Bhaktapur': '25', 'Lamjung': '37', 'Sunsari': '10',
    'Kapilbastu': '47', 'Kanchanpur': '75',
    'Kailali': '71', 'Sindhupalchowk': '23',
    'Jumla': '54', 'Morang': '09', 'Dolpa': '52',
    'Surkhet': '64', 'Siraha': '16', 'Nawalparasi': '42',
    'Chitwan': '35', 'Jhapa': '04', 'Baitadi': '73',
    'Achham': '68', 'Makawanpur': '34', 'Bara': '32',
    'Okhaldhunga': '12', 'Rukum': '57', 'Darchula': '72',
    'Tehrathum': '08', 'Nuwakot': '29', 'Bajhang': '69',
    'Mustang': '48', 'Parbat': '50', 'Udayapur': '14',
    'Illam': '03', 'Manang': '39', 'Palpa': '43',
    'Dolakha': '17', 'Jajarkot': '62', 'Mahottari': '21',
    'Kavre': '24', 'Gorkha': '36'
}


class RowMaker:
    __metaclass__ = ABCMeta

    @abstractmethod
    def make_row(self, geo_level, geo_code, value_name, total):
        pass

    @abstractmethod
    def national_totals(self, district_rows):
        pass


class SingleFieldRowMaker(RowMaker):

    def __init__(self, field_name):
        self.field_name = field_name

    def make_row(self, geo_level, geo_code, value_name, total):
        return {
            'geo_level': geo_level,
            'geo_code': geo_code,
            self.field_name: value_name,
            'total': total
        }

    def national_totals(self, district_rows):
        getter = itemgetter(self.field_name)
        return [self.make_row(
            'country', 'NP', key, sum(map(lambda i: i['total'], group)))
                for key, group in groupby(
                sorted(district_rows, key=getter), getter)]


class BySexRowMaker(RowMaker):

    def __init__(self, field_name):
        self.field_name = field_name

    def __extract_sex_from_value_name(self, value_name):
        if value_name.endswith('_MALE'):
            sex = 'male'
        elif value_name.endswith('_FEMALE'):
            sex = 'female'
        elif value_name.endswith('_BOTH_SEX'):
            sex = 'both'
        else:
            sex = None
        name = value_name.replace(
            '_BOTH_SEX', '').replace('_FEMALE', '').replace('_MALE', '')
        return name, sex

    def make_row(self, geo_level, geo_code, value_name, total):
        row = None
        value, sex = self.__extract_sex_from_value_name(value_name)
        if sex in ['male', 'female']:
            row = {
                'geo_level': geo_level,
                'geo_code': geo_code,
                self.field_name: value,
                'sex': sex,
                'total': total
            }
        return row

    def national_totals(self, district_rows):
        totals = []
        getter = itemgetter(self.field_name, 'sex')
        for key, group in groupby(sorted(district_rows, key=getter), getter):
            totals.append(
                {
                    'geo_level': 'country',
                    'geo_code': 'NP',
                    self.field_name: key[0],
                    'sex': key[1],
                    'total': sum(map(lambda i: i['total'], group))
                }
            )

        return totals


class CsvConverter:

    def __init__(self, row_maker, total_all_rows=False, excluded_columns=[]):
        self.row_maker = row_maker
        self.total_all_rows = total_all_rows
        self.excluded_columns = excluded_columns

    def convert_csv(self, districts_dir, output_file, field_names, csv_name):
        def get_immediate_subdirectories(a_dir):
            return [name for name in os.listdir(a_dir)
                    if os.path.isdir(os.path.join(a_dir, name))]

        def build_csv_location(district_name):
            return '{}/{}/{}'.format(districts_dir,
                                     district_name, csv_name)

        csv_file_names = list(map(build_csv_location,
                                  get_immediate_subdirectories(districts_dir)))
        district_rows = []

        for csv_file in csv_file_names:
            district_geo_code = names_to_geo_ids[csv_file.split('/')[-2]]
            with open(csv_file, 'r') as data:
                if self.total_all_rows:
                    total_dict = {}
                    reader = csv.DictReader(data)
                    for row in reader:
                        if 'TOTAL' == row['VDC/MUNICIPALITY']:
                            raise Exception('Unexpected total found')
                        row.pop('VDC/MUNICIPALITY')
                        for column in self.excluded_columns:
                            row.pop(column)
                        for key, value in row.items():
                            if key in total_dict:
                                total_dict[key] += int(value)
                            else:
                                total_dict[key] = int(value)
                    for key, value in total_dict.items():
                        row = self.row_maker.make_row('district',
                                                      district_geo_code,
                                                      key,
                                                      value
                                                      )
                        if row:
                            district_rows.append(row)

                else:
                    all_lines = data.readlines()
                    headers = all_lines[0].split(',')[1:]
                    totals = all_lines[-1].split(',')[1:]

                    for idx, header in enumerate(headers):
                        value_name = header.strip(' \t\n\r')
                        if not [val for val in [header, value_name] if
                                val in self.excluded_columns]:
                            try:
                                district_total = int(
                                    totals[idx].strip(' \t\n\r'))
                            except ValueError as err:
                                print('Error in {}, column {}'.format(
                                    csv_file, header
                                ))
                                raise err
                            row = self.row_maker.make_row('district',
                                                          district_geo_code,
                                                          value_name,
                                                          district_total
                                                          )
                            if row:
                                district_rows.append(row)

        all_rows = district_rows + self.row_maker.national_totals(
            district_rows)

        all_rows = sorted(all_rows, key=lambda x: x.get('geo_code'))
        with open(output_file, 'w') as csv_out:
            csv_keys = field_names
            writer = csv.DictWriter(csv_out, fieldnames=csv_keys)
            writer.writeheader()
            for row in all_rows:
                writer.writerow(row)

        print('Done!')


def main(args):
    indir = ''
    outputcsv = ''
    fieldname = ''
    csvname = ''
    by_sex = False
    total_all_rows = False
    excludedcolumns = []
    try:
        opts, args = getopt.getopt(args, 'hi:o:f:c:ste:',
                                   ['indir=', 'outputcsv=',
                                    'fieldname=', 'csvname=',
                                    'bysex', 'totalrows',
                                    'excludedcolumns='])
    except getopt.GetoptError:
        print('python districtnames.py -i <indir> -o <outputcsv> '
              '-f <fieldname> -c <csvname> -s -t -e <excludedcolumns>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('python districtnames.py -i <indir> -o <outputcsv> '
                  '-f <fieldname> -c <csvname> -s -t -e <excludedcolumns>')
            sys.exit()
        elif opt in ('-i', '--indir'):
            indir = arg
        elif opt in ('-o', '--outputcsv'):
            outputcsv = arg
        elif opt in ('-f', '--fieldname'):
            fieldname = arg
        elif opt in ('-c', '--csvname'):
            csvname = arg
        elif opt in ('-s', '--csvname'):
            by_sex = True
        elif opt in ('-t', '--totalrows'):
            total_all_rows = True
        elif opt in ('-e', '--excludedcolumns'):
            excludedcolumns = arg.split(',')

    if by_sex:
        row_maker = BySexRowMaker(fieldname)
        rows = ['geo_code', 'geo_level', fieldname, 'sex', 'total']
    else:
        row_maker = SingleFieldRowMaker(fieldname)
        rows = ['geo_code', 'geo_level', fieldname, 'total']
    converter = CsvConverter(row_maker, total_all_rows=total_all_rows,
                             excluded_columns=excludedcolumns)
    converter.convert_csv(indir, outputcsv, rows, csvname)


if __name__ == '__main__':
    main(sys.argv[1:])
