# Election scraper

## Projekt 3 for Engeto Python Akademi

## Project Description
The goal is to extract the results of the parliamentary elections in 2017 for a selected district from this link (in the column 'Selection of Municipality') and save them into a CSV file.

## Library Installation"
Libraries used in the code are stored in the requirements.txt file.
To install the libraries from the file, you can use the command "pip install -r requirements.txt". This command will install all the libraries listed in the requirements.txt file into your Python environment.

## Running the project
The maimn.py file is executed from the command line and requires two arguments.

python main.py <territorial_unit_link> <output_file>

The output is a .csv file with election results.

You can open the csv file in applications like Libre Office, using the Windows cp1250 encoding and comma as the delimiter(On Windows OS).

## Sample project:
Results for the Děčín district:

argument -> https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=6&xnumnuts=4201
argument -> data.csv

## Running program:

python main.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=6&xnumnuts=4201" data.csv

## Part of program execution

Downloading data from the given URL: https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=6&xobec=562912&xvyber=4201
Downloading data from the given URL: https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=6&xobec=562921&xvyber=4201
Downloading data from the given URL: https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=6&xobec=562939&xvyber=4201
Downloading data from the given URL: https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=6&xobec=562947&xvyber=4201
SAVING DATA TO A FILE: data.csv
UKONČUJI election scraper
