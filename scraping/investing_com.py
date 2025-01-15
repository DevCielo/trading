import pandas as pd
import datetime as dt
from scraping.utils import get_soup_from_url, get_soup_from_file
import time

pd.set_option('display.expand_frame_repr', False)

def get_request_headers():
    return {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.investing.com',
        'Referer': 'https://www.investing.com/technical/technical-analysis',
        'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'en-GB,en;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache'
    }

def get_pivot_points(table):
    data_row = table.find('tbody').find('tr')
    return [td.text for td in data_row.find_all('td')[1:]]

def calculate_percentages(total_buy, total_sell):
    percent_bullish = (total_buy / (total_buy + total_sell)) * 100
    return percent_bullish, 100 - percent_bullish

def get_technical_values(element):
    buy = element.find("i", id="maBuy").text
    sell = element.find("i", id="maSell").text
    return int(buy), int(sell)

def parse_technical_data(soup):
    pair_name = soup.find("a", id="quoteLink").text
    pair_name = pair_name.replace("/", "_")

    technical_box = soup.find("div", id='techStudiesInnerBoxRight')
    summary_tables = technical_box.find_all("div", class_="summaryTableLine")

    ma_buy, ma_sell = get_technical_values(summary_tables[0])
    ti_buy, ti_sell = get_technical_values(summary_tables[1])

    percent_bullish, percent_bearish = calculate_percentages(ma_buy + ti_buy, ma_sell + ti_sell)

    table = soup.find("table", {'class': 'genTbl closedTbl crossRatesTbl'})

    pivot_values = get_pivot_points(table)

    return dict(
        pair_name=pair_name,
        ma_buy=ma_buy,
        ma_sell=ma_sell,
        ti_buy=ti_buy,
        ti_sell=ti_sell,
        percent_bullish=percent_bullish,
        percent_bearish=percent_bearish,
        S3 = pivot_values[0],
        S2 = pivot_values[1],
        S1 = pivot_values[2],
        pivot = pivot_values[3],
        R1 = pivot_values[4],
        R2 = pivot_values[5],
        R3 = pivot_values[6],
    )

def investing_com_fetch(pair_id, time_frame):
    #soup = get_soup_from_file("investing_com")

    url = "https://www.investing.com/technical/Service/GetStudiesContent"

    payload = f"pairID={pair_id}&period={time_frame}"

    soup = get_soup_from_url(url, verb="post", data=payload, extra_headers=get_request_headers())

    data = parse_technical_data(soup)
    data['pair_id'] = pair_id
    data['time_frame'] = time_frame
    data['updated']=dt.datetime.now(dt.timezone.utc)
    return data

def investing_com(pair_ids=range(1, 4), timeframes=[3600, 86400], delay=1):
    data = []
    for pair_id in pair_ids:
        for timeframe in timeframes:
            data.append(investing_com_fetch(pair_id, timeframe))
            time.sleep(delay)
    
    return pd.DataFrame(data)