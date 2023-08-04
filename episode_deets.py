import os
import csv
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

        if not episode_url == "https://www.imdb.com/title/None/":
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
    with open(filename, 'w', newline='') as f:
        for episode in episode_list:
            print(episode)
            writer = csv.writer(f)
            row = [episode['Episode Number'], episode['Airing Year'], episode['Episode Title'], episode['Rating'], episode['Plot']]
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
    print("showName.txt is missing", "Fail")
    exit(1)
with open(file_name, 'r') as file:
    for line in file:
        showName = line.strip()
        if showName == "":
            print("showName.txt is empty", "Fail")
            exit(1)

# replaces spaces with %20
showName = showName.replace(" ", "%20")
url = 'https://www.imdb.com/find/?q=' + showName

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
driver.get(url)

# Clicks on the first result
if len(driver.find_elements_by_class_name("ipc-metadata-list-summary-item__t")) == 0:
    print("No results found", "Fail")
    exit(1)
driver.find_elements_by_class_name("ipc-metadata-list-summary-item__t")[0].click()

# Gets the show ID from the URL
showId = driver.current_url.split("/")[4]
# Creates the URL for the episodes
url = 'https://www.imdb.com/search/title/?series=' + showId + '&view=simple&count=250&sort=user_rating,desc&ref_=tt_eps_rhs_sm'

# Example usage
episodes = scrape_imdb_show_episodes(url)
print("Scraping Done")
# Write the episode details to CSV
write_to_csv(episodes, 'testing.csv')
print("Writing Done")