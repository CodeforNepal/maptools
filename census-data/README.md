# Use

The scripts here are for converting data in the [census-data project](https://github.com/Code4Nepal/census-data) into a form that can be inserted into tables in the [nepalmap project](https://github.com/Code4Nepal/nepalmap_app).

# `singlefieldwithcount.py`

Used for converting a data set that has only one field with counts for each value. Example usage:

`python census-data/singlefieldwithcount.py -o cookingfuel.csv -i /path/to/census-data/districts -c COOKING_FUEL.csv -f "main type of cooking fuel"`

In this case, we are looking for data in the `COOKING_FUEL.csv` in each of the districts, and we want the main field to be called "main type of cooking fuel", where is the name of the column in the database for Nepal Map.