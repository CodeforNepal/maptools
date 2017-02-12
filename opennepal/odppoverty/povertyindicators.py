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


def pops_for_indicator(rowname):
    # 'District'
    # 'Population'
    # rowname
    def pops_for_row(percent_dict):
        in_condition = int(percent_dict['Population'] * percent_dict[rowname])
        not_in_condition = percent_dict['Population'] - in_condition
        return [
            {
                'geo_level': 'district',
                'geo_code': percent_dict['District'],
                rowname: 'NO',
                'total': in_condition
            },
            {
                'geo_level': 'district',
                'geo_code': percent_dict['District'],
                rowname: 'YES',
                'total': not_in_condition
            }
        ]
    return pops_for_row


def national_totals(district_rows, rowname):
    getter = itemgetter(rowname)
    return [{
                'geo_level': 'country',
                'geo_code': 'NP',
                rowname: key,
                'total': sum(map(lambda i: i['total'], group))
            }
            for key, group in groupby(sorted(district_rows, key=getter),
                                      getter)]


def convert_csv(populationfile, indicatorfile, indicator, rowname, outputfile):
    print('Input file: {}, \nOutput file: {}'.format(populationfile,
                                                     outputfile))
    pop_keys = ['District', 'Indicators', 'Value']
    indicator_keys = ['District', 'Sub Group', 'Value']
    with open(populationfile, 'r') as pop_data, \
            open(indicatorfile, 'r') as indicator_data:
        pop_reader = csv.DictReader(pop_data)
        indicator_reader = csv.DictReader(indicator_data)

        population_dicts = [{desired_key: row[desired_key] for desired_key
                             in pop_keys} for row in pop_reader
                            if row['Year AD'] == '2011' and
                            row['Indicators'] == 'Population']

        indicator_dicts = [{desired_key: row[desired_key] for desired_key
                            in indicator_keys} for row in indicator_reader
                           if row['Sub Group'] == indicator]

        population_dicts.sort(key=itemgetter('District'))
        indicator_dicts.sort(key=itemgetter('District'))

        pop_and_indicator_rows = []
        for key, group in groupby(population_dicts,
                                  lambda row: row['District']):
            pop_dict = list(group)[0]
            indicator_dict = list(filter(
                lambda r: r['District'] == key,
                indicator_dicts))[0]
            blended = {
                'District': names_to_geo_ids[key],
                pop_dict['Indicators']: int(float(pop_dict['Value'])),
                rowname: round(float(indicator_dict['Value']) * 0.01, 3)
            }
            pop_and_indicator_rows.append(blended)

        district_rows = [item for sublist in
                         list(map(pops_for_indicator(rowname),
                                  pop_and_indicator_rows))
                         for item in sublist]

        all_rows = district_rows + national_totals(district_rows, rowname)

        a = 'a'
    sorted_rows = sorted(all_rows, key=lambda x: (x.get('geo_code'),
                                                  x.get('poverty')))

    with open(outputfile, 'w') as csv_out:
        csv_keys = sorted_rows[0].keys()
        writer = csv.DictWriter(csv_out, fieldnames=csv_keys)
        writer.writeheader()
        for row in sorted_rows:
            writer.writerow(row)


def main(args):
    populationfile = ''
    indicatorfile = ''
    indicator = ''
    rowname = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(args, 'hi:d:m:n:o:',
                                   ['populationfile=',
                                    'indicatorfile=',
                                    'indicator=',
                                    'rowname=',
                                    'outputfile='])
    except getopt.GetoptError:
        print('python povertyindicators.py -i <populationfile> '
              '-d <indicatorfile> -m <indicator> -n <rowname> '
              '-o <outputfile> ')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('python povertyindicators.py -i <populationfile> '
                  '-d <indicatorfile>  -m <indicator> -n <rowname> '
                  '-o <outputfile>')
            sys.exit()
        elif opt in ('-i', '--populationfile'):
            populationfile = arg
        elif opt in ('-d', '--indicatorfile'):
            indicatorfile = arg
        elif opt in ('-m', '--indicator'):
            indicator = arg
        elif opt in ('-n', '--rowname'):
            rowname = arg
        elif opt in ('-o', '--outputfile'):
            outputfile = arg

    convert_csv(populationfile, indicatorfile, indicator, rowname, outputfile)

    print('Done!')

if __name__ == '__main__':
    main(sys.argv[1:])
