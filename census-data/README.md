# Use

The scripts here are for converting data in the [census-data project](https://github.com/Code4Nepal/census-data) into a form that can be inserted into tables in the [nepalmap project](https://github.com/Code4Nepal/nepalmap_app).

# `csvconverter.py`

Used for converting a data set. 

## Arguments
`-i` requires an argument of the path to the directory which holds the district directories, probably `/path/to/census-data/districts`

`-c` requires an argument of the name of the CSV files that will be consumed. There should be one named this in every district directory

`-o` requires an argument of the output file name

`-v` requires an argument identifying the location of a JSON-formatted file that contains mappings for assigning geo ids to village development councils

`-s` optional, no argument, is used to identify a data set that has data separated by gender, defaults to false.

`-e` optional, takes an argument of a comma-separated list of columns to exclude

`-n` optional, takes an argument of a comma-separated list of columns to use for the total, must be used with the `-k` option

`-k` optional, takes an argument of a name to give the value that was generated from the `-n` option, must be used with the `n` option


Example usages:

`python census-data/csvconverter.py -o cookingfuel.csv -i /path/to/census-data/districts -c COOKING_FUEL.csv -v vdc_geo_code_mappings.json -f "main type of cooking fuel"`

* We are looking for data in the `COOKING_FUEL.csv` in each of the districts
* We want the main field to be called "main type of cooking fuel", the name of the column in the database for Nepal Map.

`python census-data/csvconverter.py -o educationlevel.csv -i /path/to/census-data/districts -c POPULATION_EDUCATION_LEVEL_PASSED.csv -v vdc_geo_code_mappings.json -f "education level passed" -s`

* We are looking for data in the `POPULATION_EDUCATION_LEVEL_PASSED.csv` in each of the districts. 
* We want the main field to be called "education level passed", the name of the column in the database for Nepal Map. 
* The data is divided by gender.

`python census-data/csvconverter.py -o literacy.csv -i /path/to/census-data/districts -c POPULATION_LITERACY_STATUS_AND_SEX_5_AND_ABOVE.csv -v vdc_geo_code_mappings.json -f "literacy" -s -e POPULATION_5_AND_ABOVE_BOTH_SEX,POPULATION_5_AND_ABOVE_MALE,POPULATION_5_AND_ABOVE_FEMALE,LITERACY_RATE_BOTH_SEX,LITERACY_RATE_MALE,LITERACY_RATE_FEMALE`

* We are looking for data in the `POPULATION_LITERACY_STATUS_AND_SEX_5_AND_ABOVE.csv` in each of the districts.
* We want the main field to be called "literacy", the name of the column in the database for Nepal Map. 
* The data is divided by gender.
* We want to exclude the columns `POPULATION_5_AND_ABOVE_BOTH_SEX`, `POPULATION_5_AND_ABOVE_MALE`, `POPULATION_5_AND_ABOVE_FEMALE` ,`LITERACY_RATE_BOTH_SEX` , `LITERACY_RATE_MALE`, and `LITERACY_RATE_FEMALE`

`python census-data/csvconverter.py -o facilities.csv -i /path/to/census-data/districts -c HOUSEHOLD_FACILITY.csv -v vdc_geo_code_mappings.json -f "household facilities" -n "NO_FACILITY,AT_LEAST_ONE,NOT_STATED" -k "TOTAL_HOUSEHOLDS"`

* We want to take as the total the cumulative value of the columns `NO_FACILITY`, `AT_LEAST_ONE`, and `NOT_STATED`
* We want to put that total in a column called `TOTAL_HOUSEHOLDS`
