import time
import pandas as pd
import datetime as dt
from dateutil.parser import parse
from scraping.utils import get_soup_from_file, get_soup_from_url
from db.db import DataDB
import random


def get_date(c):
    tr = c.find("tr")
    ths = tr.find_all("th")
    for th in ths:
        if th.has_attr('colspan'):
            date_str = th.text.strip()
            return parse(date_str)
    return None


def get_data_point(element, key):
    d = element.find(id=key)
    if d:
        return d.text
    return ''


def get_data_for_key(tr, key):
    return tr.attrs.get(key, '').strip() 


def get_data_dict(item_date, tr):
    return dict(
        date=item_date,
        country=get_data_for_key(tr, 'data-country'),
        category=get_data_for_key(tr, 'data-category'),
        event=get_data_for_key(tr, 'data-event'),
        symbol=get_data_for_key(tr, 'data-symbol'),
        actual=get_data_point(tr, 'actual'),
        previous=get_data_point(tr, 'previous'),
        forecast=get_data_point(tr, 'forecast')
    )


def get_fx_calendar(from_date):

    #soup = get_soup_from_file("fx_calendar")
    fr_d_str = dt.datetime.strftime(from_date, "%Y-%m-%d 00:00:00")
    to_date = from_date + dt.timedelta(days=6)
    to_d_str = dt.datetime.strftime(to_date, "%Y-%m-%d 00:00:00")

    cal_cust_range=f"cal-custom-range={fr_d_str}|{to_d_str}"
    cal_importance="calendar-importance=3"

    headers = {
        "Cookie": f"{cal_importance}; {cal_cust_range}; TEServer=TEIIS2; cal-timezone-offset=0;"
    }

    soup = get_soup_from_url(
        "https://tradingeconomics.com/calendar",
        extra_headers=headers
    )

    table = soup.find("table", id="calendar")
    
    last_header_date = None
    final_data = []

    for c in table.children:
        if c.name == 'thead':
            if 'class' in c.attrs and 'hidden-head' in c.attrs['class']:
                continue
            last_header_date = get_date(c)
        elif c.name == "tr":
            final_data.append(
                get_data_dict(last_header_date, c)
            )

    return final_data

def fx_calendar():
    # final_data = []

    start = parse('2024-12-05T00:00:00Z')
    end = parse('2025-01-12T00:00:00Z')

    database = DataDB()

    while start < end:
        data = get_fx_calendar(start)
        print(start, len(data))
        database.add_many(DataDB.CALENDAR_COLL, data)
        start = start + dt.timedelta(days=7)
        time.sleep(random.randint(1,4))

    #df_cal = pd.DataFrame.from_dict(final_data)
    #df_cal.drop_duplicates(
        #subset=['date', 'country', 'event'],
        #inplace=True
    #)

    #print(df_cal.head())
    #print(df_cal.tail())