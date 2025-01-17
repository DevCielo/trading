from scraping.utils import get_soup_from_file, get_soup_from_url

def bloomberg_com():
    # soup = get_soup_from_file("bloomberg")

    soup = get_soup_from_url("https://www.reuters.com/business/finance/")


    articles = []

    #cards = soup.find_all('div', class_=lambda x: x and 'media-story-card__body' in x)
    # ^ for partially matches
    cards = soup.select('[class^="media-story-card__body"]')

    for card in cards:
        #headline_link = card.select_one('a[data-testid="Heading"]')
        headline_link = card.find('a', attrs={'data-testid': 'Heading'})
        if headline_link:
            articles.append(dict(
                headline=headline_link.text,
                link="https://www.reuters.com" + headline_link['href']
            ))

    return articles

            
