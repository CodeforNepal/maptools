# Use

The scripts here are for converting data in the [census-data project](https://github.com/Code4Nepal/census-data) into a form that can be inserted into tables in the [nepalmap project](https://github.com/Code4Nepal/nepalmap_app).

# `csvconverter.py`

Used for converting a data set. 

## Arguments
`-i` requires an argument of the path to the directory which holds the district directories, probably `/path/to/census-data/districts`

`-c` requires an argument of the name of the CSV files that will be consumed. There should be one named this in every district directory

`-o` requires an argument of the output file name

`-s` optional, no argument, is used to identify a data set that has data separated by gender, defaults to false.

`t` optional, no argument, is used to identify a data set that requires totaling all of the rows in each CSV, defaults to false.


Example usages:

`python census-data/csvconverter.py -o cookingfuel.csv -i /path/to/census-data/districts -c COOKING_FUEL.csv -f "main type of cooking fuel"`

In this case, we are looking for data in the `COOKING_FUEL.csv` in each of the districts, and we want the main field to be called "main type of cooking fuel", the name of the column in the database for Nepal Map.

`python census-data/csvconverter.py -o educationlevel.csv -i /path/to/census-data/districts -c POPULATION_EDUCATION_LEVEL_PASSED.csv -f "main type of cooking fuel" -s -t`

In this case, we are looking for data in the `POPULATION_EDUCATION_LEVEL_PASSED.csv` in each of the districts, and we want the main field to be called "main type of cooking fuel", the name of the column in the database for Nepal Map. The data is divided by gender and we must calculate the totals.
