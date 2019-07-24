# Parses XML from this location:
# https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=billrates

from decimal import Decimal
from lxml import etree as ET
import pprint
import requests
import time
import os
import datetime
from datetime import timedelta

MATUIRITY_TENOR = [4, 8, 13, 26, 52]
TREASURY_URL = 'http://data.treasury.gov/feed.svc/DailyTreasuryBillRateData?$filter=month(INDEX_DATE)%20ge%206%20and%20year(INDEX_DATE)%20eq%202019'

def get_latest_xml(url, filename):
    # TODO: Add error handling
    #GETs url and saves as filename
    resp = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(resp.content)


def parse_treasury_xml(xmlfile):
    # TODO: Add error handling
    """
    Parses a treasury XML file like the one returned from:
      https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=billrates
    which is at URL:
      http://data.treasury.gov/feed.svc/DailyTreasuryBillRateData?$filter=month(INDEX_DATE)%20eq%207%20and%20year(INDEX_DATE)%20eq%202019
    and returns a dictionary with the quote date and discount for each maturity
    (4, 8, 13, 26, 52).
    :param xmlfile: The filename of the XML source file to parse.
    :return: { "quote_date": Date(Y,M,D), "quote_date_string": "...",
               4: { "discount": 1.2, "discount_decimal": Decimal(1.2),
                    "maturity": Date(Y,M,D), "maturity_string": "..." },
               ...}
    """

    # Parse the file
    tree = ET.parse(xmlfile)
    # Get the main element
    root = tree.getroot()
    latest_entry = None

    for item in root.findall('entry', root.nsmap):
        cont = item.find('content', root.nsmap)
        props = cont.find('m:properties', root.nsmap)
        if latest_entry is None:
            latest_entry = props
        # String comparison should work for strings in form YYYY-MM-DDThh:mm:ss
        elif latest_entry.find('d:INDEX_DATE', root.nsmap).text < props.find('d:INDEX_DATE', root.nsmap).text:
            latest_entry = props

    date_format = '%Y-%m-%dT%H:%M:%S'
    quote_date = latest_entry.find('d:INDEX_DATE', root.nsmap).text
    retval = {
        "quote_date_string": quote_date,
        "quote_date": datetime.datetime.strptime(quote_date, date_format).date()
    }
    for wk in MATUIRITY_TENOR:
        discount = latest_entry.find(f'd:CS_{wk}WK_CLOSE_AVG', root.nsmap).text
        maturity = latest_entry.find(f'd:MATURITY_DATE_{wk}WK', root.nsmap).text
        rates = {
            "discount_decimal": Decimal(discount),
            "discount": float(discount),
            "maturity_string": maturity,
            "maturity": datetime.datetime.strptime(maturity, date_format).date()
        }
        retval[wk] = rates

    return retval


def calc_discount(rates, for_date: datetime.date):
    """
    Calculates the discount rate to be used for a T-Bill with the specified maturity
    date. Should not be more than 52 weeks away.

    WARNING: THIS USES FLOATING POINT MATH (Python floats which are C doubles).

    Uses the 4-week rate for anything shorter, and the 52-week rate for anything longer.

    Note that the number of days away for each of the maturities may not be exactly
    4, 8, 13, 26 or 52 weeks because the maturities are only on certain days,
    so this accounts for the actual number of days until each maturity date when
    interpolating. Uses linear interpolation for anything not on an exact maturity date.

    :param rates: as returned by parse_treasury_xml()
    :param for_date: Should be a datetime.date
    :return: a floating point discount rate to use to the face value
    """
    today = datetime.date.today()

    # Number of days into the future the various maturity dates are...
    days = []
    discounts = []

    for wk in MATUIRITY_TENOR:
        maturity = rates[wk]['maturity']
        diff = maturity - today
        days.append(diff.days)
        discounts.append(rates[wk]['discount'])

    days_until_date = (for_date - today).days

    # Determine the discount to use. If fewer than the initial number
    # of days until maturity, use the lowest amount.
    min_days = days[0]
    if days_until_date <= min_days:
        return discounts[0]

    # Otherwise, step thru until we are below that number of days
    last_rate = None
    last_days = None
    for wk, d, r in zip(MATUIRITY_TENOR, days, discounts):
        if d < days_until_date:
            last_rate = r
            last_days = d
            continue
        if days_until_date == d:
            # Exactly at the boundaries
            return r
        elif days_until_date > d:
            continue
        # Linear interpolation between the last two
        days_between = d - last_days
        days_over = days_until_date - last_days
        rate_difference = r - last_rate
        lerp = last_rate + rate_difference * days_over / days_between
        return lerp

    # It's more than the number of days - which shouldn't happen
    return discounts[len(discounts) - 1]

if __name__ == "__main__":
    # TODO: Add error handling (especially deleting the temporary file in case of error)
    now = time.time()
    # TODO: Use temporary file system (tempfile) - or just load into memory?
    filename = f'treasuryrates-{now}.xml'
    # TODO: Calculate URL with current month and year
    get_latest_xml(TREASURY_URL, filename)
    # TODO: If URL didn't get any rates, use previous month
    rates = parse_treasury_xml(filename)
    pp = pprint.PrettyPrinter(indent=4)
    print("\nRates:")
    pp.pprint(rates)
    os.remove(filename)

    today = datetime.date.today()
    for i_mat in range(0, 366):
        mat = today + timedelta(days=i_mat)
        disc = calc_discount(rates, mat)
        print('Discount for maturity %s: %.16f' % (mat, disc))

# TODO: Take face_value and maturity_date on command line and
# return current_value and discount_rate for that maturity.
