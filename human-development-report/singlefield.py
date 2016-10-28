import csv
import getopt
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
    'Bhojpur': '06', 'Dhanusa': '20', 'Panchthar': '02',
    'Kalikot': '55', 'Tanahu': '38', 'Bardiya': '66',
    'Lalitpur': '26', 'Humla': '56', 'Kaski': '40',
    'Syangja': '41', 'Dadeldhura': '74', 'Dhading': '30',
    'Pyuthan': '59', 'Taplejung': '01', 'Rolpa': '58',
    'Bhaktapur': '25', 'Lamjung': '37', 'Sunsari': '10',
    'Kapilbastu': '47', 'Kanchanpur': '75',
    'Kailali': '71', 'Sindhupalchok': '23',
    'Jumla': '54', 'Morang': '09', 'Dolpa': '52',
    'Surkhet': '64', 'Siraha': '16', 'Nawalparasi': '42',
    'Chitwan': '35', 'Jhapa': '04', 'Baitadi': '73',
    'Achham': '68', 'Makwanpur': '34', 'Bara': '32',
    'Okhaldhunga': '12', 'Rukum': '57', 'Darchula': '72',
    'Tehrathum': '08', 'Nuwakot': '29', 'Bajhang': '69',
    'Mustang': '48', 'Parbat': '50', 'Udayapur': '14',
    'Ilam': '03', 'Manang': '39', 'Palpa': '43',
    'Dolakha': '17', 'Jajarkot': '62', 'Mahottari': '21',
    'Kavrepalanchok': '24', 'Gorkha': '36'
}


def convert_csv(input_file, output_file, column, separator):
    rows = []
    with open(input_file, 'r') as data:
        reader = csv.DictReader(data, delimiter=separator)
        for row in reader:
            geo_code = names_to_geo_ids[row['district']]
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
