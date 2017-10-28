import csv
import getopt
import shapefile

import sys
from collections import namedtuple


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

facility_type_map = {
    'Hospital': "HOSPITAL",
    'Private Hospital': "PRIVATE_HOSPITAL",
    'Zonal Hospital': "ZONAL_HOSPITAL",
    'Central Hospital': "CENTRAL_HOSPITAL",
    'Health Center': "HEALTH_CENTER",
    'Primary Health Center': "PRIMARY_HEALTH_CENTER", 
    'Supply Center': "SUPPLY_CENTER",
    'District Center': "DISTRICT_CENTER",
    'Sub Center': "SUB_CENTER",
    'Laxmipur': "LAXMIPUR",
    'Refugee Camp': "REFUGEE_CAMP",
    'DIstrict Cold Room': "DISTRICT_COLD_ROOM",
    'Distict Cold Room': "DISTRICT_COLD_ROOM",
    'District Cold Room': "DISTRICT_COLD_ROOM",
    'DAHC': "DAHC",
    'RMS': "RMS",
    'DPHO': "DPHO",
    'D(P)HO': "DPHO",
    'Health Post': "HEALTH_POST",
    'Primary Health Post': "PRIMARY_HEALTH_POST",
    'Sub Health Post': "SUB_HEALTH_POST",
    'Health Care Center': "HEALTH_CARE_CENTER",
    'Ayurvedic Aushadhalaya': "AYURVEDIC_AUSHADHALAYA",
    'District Ayurvedic HC': "DISTRICT_AYURVEDIC_HC"
}

def national_totals(district_rows):

    all_facilities = set([val for _, val 
        in facility_type_map.iteritems()])

    return [{
        'geo_level': 'country',
        'geo_code': 'NP',
        'facility_type': facility,
        'total': sum([
            district['total'] for district
                in district_rows if 
                    district['facility_type'] ==
                        facility
            ])
        } for facility in all_facilities
    ]

def get_data_from_shapefile(filename):
    sf = shapefile.Reader(filename)

    data = {}
    for rec in sf.records():
        district = rec[2]
        if district in names_to_geo_ids:
            district_id = names_to_geo_ids[district]
            if district_id not in data:
                data[district_id] = {}

            facility_type = rec[1]

            if facility_type in facility_type_map:
                facility_type = facility_type_map[facility_type]
                data[district_id][facility_type] = data[district_id][facility_type] + 1 if (
                    facility_type in data[district_id]) else 1
            else:
                print("{0} not in facility_type_map".format(facility_type))

        else:
            print("Unknown district: {0}".format(district))

    return data

def extract_each_district(district_data):

    district_rows = []
    facilities = set([val for _, val
        in facility_type_map.iteritems()])

    districts = set([val for _, val
        in names_to_geo_ids.iteritems()])

    for district in districts:
        if district in district_data:
            this_district = district_data[district]
            for facility in facilities:
                if facility in this_district:
                    count = this_district[facility]
                else:
                    count = 0

                district_rows.append({
                    'geo_level': 'district',
                    'geo_code': district,
                    'facility_type': facility,
                    'total': count
                })

    return district_rows

def convert_to_csv(inputfile, outputfile):
    print('Input file: {}\nOutput file: {}'.format(inputfile, outputfile))

    district_data = get_data_from_shapefile(inputfile)

    # find any missing districts
    all_districts = set([val for _, val 
        in names_to_geo_ids.iteritems()])

    districts_with_data = set([key for key, _ 
        in district_data.iteritems()])

    print("Districts without data: {0}".format(
          list(all_districts - districts_with_data)
        )
    )

    district_csv_data = extract_each_district(district_data)

    with open(outputfile, 'w') as csv_out:
        csv_keys = ['geo_code', 'geo_level', 'facility_type', 'total']
        writer = csv.writer(csv_out)
        writer.writerow(csv_keys)
        for row in national_totals(district_csv_data) + district_csv_data:
            writer.writerow([
                row[key] for key in csv_keys 
            ])

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
            print('python health.py '
                  '-i <inputfile> '
                  '-o <outputfile> ')
            sys.exit()
        elif opt in ('-i', '--inputfile'):
            inputfile = arg
        elif opt in ('-o', '--outputfile'):
            outputfile = arg

    convert_to_csv(inputfile, outputfile)
    print('Done!')

if __name__ == '__main__':
    main(sys.argv[1:])
