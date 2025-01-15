from scraping.utils import get_soup_from_file, get_soup_from_url
import pandas as pd
import re


def get_perc_from_style(style):
    return re.search(r'(\d+)', style).group()

def get_popularity(tr):
    popularity = "-"
    possible_rows = tr.find_all('div', class_='progress-bar')

    if len(possible_rows) < 3:
        return popularity

    popularity_data = possible_rows[2]

    if popularity_data.has_attr('style'):
        popularity = get_perc_from_style(popularity_data['style'])

    return popularity

def get_bearish_bullish_perc(tr):
    bearish = tr.find('div', class_='progress-bar-danger')
    bullish = tr.find('div', class_='progress-bar-success')

    bearish_perc = get_perc_from_style(bearish['style'])
    bullish_perc = get_perc_from_style(bullish['style'])

    return bearish_perc, bullish_perc

def get_price(prefix, tr, pair_name):
    id_price = f'{prefix}PriceCell{pair_name}'
    id_distance = f'{prefix}DisCell{pair_name}'

    price = tr.find('span', id=id_price).text
    distance = tr.find('span', id=id_distance).text

    return price, distance 


def get_data_from_row(tr):
    pair_name = tr['symbolname']

    long_price, long_distance = get_price('long', tr, pair_name)
    short_price, short_distance = get_price('short', tr, pair_name)
    
    bearish_perc, bullish_perc = get_bearish_bullish_perc(tr)

    popularity = get_popularity(tr)

    return dict(
        pair_name=pair_name,
        long_price=long_price,
        long_distance=long_distance,
        short_price=short_price,
        short_distance=short_distance,
        bearish_perc=bearish_perc,
        bullish_perc=bullish_perc,
        popularity=popularity
    )

def run_sentiment_scrape():
    # soup = get_soup_from_file("my_fx_book")
    soup = get_soup_from_url("https://www.myfxbook.com/community/outlook")

    rows = soup.find_all('tr', class_='outlook-symbol-row')

    pair_data = []
    for r in rows:
        pair_data.append(get_data_from_row(r))
        
    sentiment_df = pd.DataFrame(pair_data)

    print(sentiment_df)