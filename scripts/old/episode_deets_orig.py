import csv
import os
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def scrape_episode_details(url):
    plot_url = url
    response = requests.get(plot_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(plot_url)
    if not plot_url == "https://www.imdb.com/title/None/":
        driver.get(plot_url + "plotsummary")
        str = driver.find_elements_by_class_name("ipc-html-content-inner-div")[1].text
        print(str)
        return str
    return ""

def scrape_imdb_show_episodes(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    episode_list = []

    episode_elements = soup.select('div.lister-item-content')
    for episode_element in episode_elements:
        episode_title_element = episode_element.select_one('a[href^="/title/"]')
        episode_title = episode_title_element.text if episode_title_element else None

        episode_number_element = episode_element.find_previous('small', class_='text-primary unbold')
        if episode_number_element:
            episode_number = episode_number_element.find_next('a', href=True).text.strip()
        else:
            episode_number = None

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
        plot = scrape_episode_details(episode_url)
        print(plot)

        episode_list.append({
            'Episode Number': episode_number,
            'Airing Year': airing_year,
            'Episode Title': episode_title,
            'Rating': rating,
            'Plot': plot
        })

    return episode_list

def write_to_csv(episode_list, filename):
    keys = episode_list[0].keys() if episode_list else []
    with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(episode_list)


chromedriver_path = './chromedriver.exe'
# url = 'https://www.imdb.com/search/title/?series=tt2345459&view=simple&count=250&sort=user_rating,desc&ref_=tt_eps_rhs_sm'  # Replace with the IMDb URL of the show
url = 'https://www.imdb.com/search/title/?series=tt0343314&view=simple&count=250&sort=user_rating,desc&ref_=tt_eps_rhs_sm'

# Set the browser options
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
driver.get(url)


# Example usage
episodes = scrape_imdb_show_episodes(url)
print("Scraping Done")
write_to_csv(episodes, 'episodesfinal.csv')
print("Writing Done")
