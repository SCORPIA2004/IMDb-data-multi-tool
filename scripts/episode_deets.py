import os
import csv
from datetime import datetime
from sys import exit
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

def scrape_episode_details(url):
    plot_url = url
    response = requests.get(plot_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(plot_url)
    if not plot_url == "https://www.imdb.com/title/None/":
        driver.get(plot_url + "plotsummary")
        str = driver.find_elements_by_class_name("ipc-html-content-inner-div")[1].text
        # print(str)
        return str
    return ""

def scrape_imdb_show_episodes(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    episode_list = []

    episode_elements = soup.select('div.lister-item-content')
    for episode_element in episode_elements:
        episode_title_element = episode_element.select_one('a[href^="/title/"]')
        show_name = episode_title_element.text if episode_title_element else None

        episode_number_element = episode_element.find_previous('small', class_='text-primary unbold')
        if episode_number_element:
            episode_name = episode_number_element.find_next('a', href=True).text.strip()
        else:
            episode_name = None

        airing_year_element = episode_element.select_one('.lister-item-year.text-muted.unbold')
        if airing_year_element:
            airing_year = airing_year_element.find_next('span').text.strip('()')
        else:
            airing_year = None

        rating = episode_element.select_one('.col-imdb-rating strong').text.strip() if episode_element.select_one('.col-imdb-rating strong') else None

        # Extract episode ID from the href attribute and construct the URL for the episode details.
        if episode_number_element:
            link =  episode_number_element.find_next('a', href=True)
            href_attribute = link['href']
            episode_id = href_attribute.split('/title/')[1].split('/')[0]
        else:
            episode_id = None
        episode_url = 'https://www.imdb.com/title/{}/'.format(episode_id)

        if not episode_url == "https://www.imdb.com/title/None/":
            plot = scrape_episode_details(episode_url)
            # print(plot)

            episode_list.append({
                'Episode Name': episode_name,
                'Airing Year': airing_year,
                'Show name': show_name,
                'Rating': rating,
                'Plot': plot
            })

    return episode_list

def write_to_csv(episode_list, filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        row = ['Episode Name', 'Airing Year', 'Show name', 'Rating', 'Plot']
        writer.writerow(row)
        for episode in episode_list:
            # logMessage(episode)
            row = [episode['Episode Name'], episode['Airing Year'], episode['Show name'], episode['Rating'], episode['Plot']]
            writer.writerow(row)

def logMessage(em, type):
    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y %H:%M:%S")
    with open("log.csv", "a", newline="") as f:
        writer = csv.writer(f)
        row = [current_time, type, em]
        writer.writerow(row)

with open("log.csv", "a", newline="") as f:
    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y %H:%M:%S")
    writer = csv.writer(f)
    row = ["Time", "Type", "Message", current_time]
    writer.writerow(row)

chromedriver_path = './chromedriver.exe'
# Set the browser options
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# check if file exists
file_name = 'showName.txt'
if not os.path.isfile(file_name):
    logMessage("showName.txt is missing", "Fail")
    exit(1)
with open(file_name, 'r') as file:
    for line in file:
        showName = line.strip()
        if showName == "":
            logMessage("showName.txt is empty", "Fail")
            exit(1)

# replaces spaces with %20
showName = showName.replace(" ", "%20")
url = 'https://www.imdb.com/find/?q=' + showName

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
driver.get(url)

# Clicks on the first result
if len(driver.find_elements_by_class_name("ipc-metadata-list-summary-item__t")) == 0:
    logMessage("No results found", "Fail")
    exit(1)
driver.find_elements_by_class_name("ipc-metadata-list-summary-item__t")[0].click()

# Gets the show ID from the URL
showId = driver.current_url.split("/")[4]
# Creates the URL for the episodes
url = 'https://www.imdb.com/search/title/?series=' + showId + '&view=simple&count=250&sort=user_rating,desc&ref_=tt_eps_rhs_sm'

# Example usage
logMessage("Scraping Started", "Success")
episodes = scrape_imdb_show_episodes(url)
logMessage("Scraping Done","Success")
# Write the episode details to CSV
write_to_csv(episodes, 'showData.csv')
logMessage("Writing Done", "Success")