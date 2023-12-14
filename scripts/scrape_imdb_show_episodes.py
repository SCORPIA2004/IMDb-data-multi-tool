    epi_elements = soup.select('div.lister-item-content')
    for epi_element in epi_elements:
        epi_title_element = epi_element.select_one('a[href^="/title/"]')
        show_name = epi_title_element.text if epi_title_element else None

        epi_number_element = epi_element.find_previous('small', class_='text-primary unbold')
        if epi_number_element:
            epi_name = epi_number_element.find_next('a', href=True).text.strip()
        else:
            epi_name = None

        airing_year_element = epi_element.select_one('.lister-item-year.text-muted.unbold')
        if airing_year_element:
            airing_year = airing_year_element.find_next('span').text.strip('()')
        else:
            airing_year = None

        rating = epi_element.select_one('.col-imdb-rating strong').text.strip() if epi_element.select_one('.col-imdb-rating strong') else None

        # Extract epi ID from the href attribute and construct the URL for the epi details.
        if epi_number_element:
            link =  epi_number_element.find_next('a', href=True)
            href_attribute = link['href']
            epi_id = href_attribute.split('/title/')[1].split('/')[0]
        else:
            epi_id = None
        epi_url = 'https://www.imdb.com/title/{}/'.format(epi_id)

        if not epi_url == "https://www.imdb.com/title/None/":
            plot = scrape_epi_details(epi_url)
            # print(plot)

            epi_list.append({
                'epi Name': epi_name,
                'Airing Year': airing_year,
                'Show name': show_name,
                'Rating': rating,
                'Plot': plot
            })
