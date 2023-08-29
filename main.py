"""
main.py: thirds project for Engeto Online Python Akademie
author: Vratislav Martin
email: abbadc@gmail.com
discord: Vratislav M (dříve: abbadc#8421)
"""
import sys
import csv
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

def get_html(url: str, verbose: bool = True) -> BeautifulSoup:
    """
    Download HTML from the specified URL and parse it using BeautifulSoup.
    """
    if verbose:
        print("Downloading data from the given URL:", url)
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, "html.parser")
    else:
        raise requests.exceptions.HTTPError(f"Server returned status code {response.status_code} for URL: {url}")

if len(sys.argv) != 3:
    print("Zadejte tři argumenty, včetně url adresy. Pro detaily čtěte readme.md")
address = sys.argv[1]
file_name = sys.argv[2]

try:
    save_html = get_html(address)
except requests.exceptions.RequestException as e:
    print("Chyba při stažení dat:", e)
    sys.exit()

def get_towns() -> list:
    """Returns a list of cities in the given district."""
    towns_search = save_html.find_all("td", class_="overflow_name")
    return [t.text for t in towns_search]

def get_urls() -> list:
    """Returns the URL address for retrieving details of individual municipalities in the requested district."""
    url_search = save_html.find_all("td", class_=["cislo", "href"])
    return [f"https://volby.cz/pls/ps2017nss/{url_town.a['href']}" for url_town in url_search]

def get_id() -> list:
    """Returns the identification numbers of individual municipalities."""
    ids = save_html.find_all("td", class_="cislo")
    return [i.text for i in ids]

def collect_parties(town_urls: list) -> list:
    """Returns a list of candidate parties in a given district."""
    with ThreadPoolExecutor() as executor:
        html_pages = executor.map(lambda url: get_html(url, False), town_urls)
        return [
            p.text
            for html_page in html_pages
            for p in html_page.find_all("td", class_="overflow_name")
        ]

def get_voters_sum(town_urls: list) -> tuple:
    """Adding the total number of registered voters, participants, and valid votes for each city to variables."""
    voters = []
    attendance = []
    valid_ones = []
    
    with ThreadPoolExecutor() as executor:
        html_villages = executor.map(lambda url: get_html(url, False), town_urls)
        data = [("sa2", voters), ("sa3", attendance), ("sa6", valid_ones)]
        for html_village in html_villages:
            for header, variable in data:
                variable.extend([v.text.replace('\xa0', ' ') for v in html_village.find_all("td", headers=header)])
    
    return (voters, attendance, valid_ones)

def list_de_votes(town_urls: list) -> list:
    """ The achieved results of political parties in individual municipalities."""
    return [
        [' '.join([v.text, '%']) for v in get_html(li).find_all("td", class_=["cislo"], headers=["t1sb4", "t2sb4"])]
        for li in town_urls
    ]

def rows_create(town_urls: list) -> list:
    """Function for generating data for a CSV file for the function below in the code."""
    voters, attendance, valid_ones = get_voters_sum(town_urls)
    towns = get_towns()
    ids = get_id()
    votes = list_de_votes(town_urls)
    
    zipped = zip(ids, towns, voters, attendance, valid_ones)
    
    return [list(data) + vote for data, vote in zip(zipped, votes)]

def election(url: str, file: str) -> None:
    """Creating a CSV file with the results obtained from the functions in the program."""
    
    try:
        town_urls = get_urls()
        
        header = ['Kód obce', 'Název obce', 'Voliči v seznamu', 'Vydané obálky', 'Platné hlasy']
        content = rows_create(town_urls)
        
        parties = collect_parties(town_urls)
        
        print("UKLÁDÁM DATA DO SOUBORU:", file)
        
        header.extend(parties)

        with open(file, 'w', newline='') as f:
            f_writer = csv.writer(f)
            f_writer.writerow(header)
            f_writer.writerows(content)

        print("UKONČUJI election scraper")
    
    except IndexError:
        print("Nastala chyba. Nejspíš máte špatný odkaz nebo jste jej zapomněli dát do uvozovek.")
    except IOError as e:
        print("Chyba při ukládání do souboru:", e)

election(address, file_name)






