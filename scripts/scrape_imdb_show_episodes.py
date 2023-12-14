def scrape_imdb_show_epis(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    epi_list = []       # contains all the episode details

    epi_elements = soup.select('div.lister-item-content')   # contains all the episode elements from the IMDb page

    for epi_element in epi_elements:
        epi_title_element = epi_element.select_one('a[href^="/title/"]')                        # contains the episode title element
        show_name = epi_title_element.text if epi_title_element else None                       # contains the episode title           

        epi_number_element = epi_element.find_previous('small', class_='text-primary unbold')   # contains the episode number element
        if epi_number_element:
            epi_name = epi_number_element.find_next('a', href=True).text.strip()                # contains the episode number
        else:
            epi_name = None

        airing_year_element = epi_element.select_one('.lister-item-year.text-muted.unbold')     # contains the episode airing year element
        if airing_year_element:
            airing_year = airing_year_element.find_next('span').text.strip('()')                # contains the episode airing year
        else:       
            airing_year = None                                                                  