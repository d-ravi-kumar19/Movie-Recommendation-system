#!/bin/bash

# Activate virtual environment
# source /path/to/your/virtualenv/bin/activate

# Install required packages
pip install -r requirements.txt

# Create migrations and apply them
python manage.py makemigrations
python manage.py migrate

# to insert data into db
python manage.py insert_data

# to populate meta data for content based recommendations
python manage.py populate_metadata

# to dump the the word vector
python manage.py dump_data

