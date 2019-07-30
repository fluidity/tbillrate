# Description
Example code that retrieves publicly-accessible T-Bill rates from the U.S. Treasury web site and calculates the current value of a T-Bill with a specified maturity date. Uses linear interpolation to determine the rate between the retrieved dates.

_NOTE: This is additional code that was not used in the pilot. This does not confirm position. The rate data is published daily._

## Execution
1. Create the virtualenv
`virtualenv env`
2. Activate the virtual environment
`source env/bin/activate`
3. Install requirements in the virtual environtment
`pip3 install -r requirements`
4. Query
`python3 testparselxml.py`

## Example
```
python3 testparselxml.py
Rates:
{   4: {   'discount': 2.09,
           'discount_decimal': Decimal('2.09'),
           'maturity': datetime.date(2019, 8, 20),
           'maturity_string': '2019-08-20T00:00:00'},
    8: {   'discount': 2.12,
           'discount_decimal': Decimal('2.12'),
           'maturity': datetime.date(2019, 9, 17),
           'maturity_string': '2019-09-17T00:00:00'},
    13: {   'discount': 2.04,
            'discount_decimal': Decimal('2.04'),
            'maturity': datetime.date(2019, 10, 24),
            'maturity_string': '2019-10-24T00:00:00'},
    26: {   'discount': 2.02,
            'discount_decimal': Decimal('2.02'),
            'maturity': datetime.date(2020, 1, 23),
            'maturity_string': '2020-01-23T00:00:00'},
    52: {   'discount': 1.89,
            'discount_decimal': Decimal('1.89'),
            'maturity': datetime.date(2020, 7, 16),
            'maturity_string': '2020-07-16T00:00:00'},
    'quote_date': datetime.date(2019, 7, 22),
    'quote_date_string': '2019-07-22T00:00:00'}
Discount for maturity 2019-07-23: 2.0899999999999999
Discount for maturity 2019-07-24: 2.0899999999999999
...
Discount for maturity 2019-08-19: 2.0899999999999999
Discount for maturity 2019-08-20: 2.0899999999999999
Discount for maturity 2019-08-21: 2.0910714285714285
Discount for maturity 2019-08-22: 2.0921428571428571
Discount for maturity 2019-08-23: 2.0932142857142857
Discount for maturity 2019-08-24: 2.0942857142857143
Discount for maturity 2019-08-25: 2.0953571428571429
Discount for maturity 2019-08-26: 2.0964285714285715
Discount for maturity 2019-08-27: 2.0975000000000001
Discount for maturity 2019-08-28: 2.0985714285714283
Discount for maturity 2019-08-29: 2.0996428571428569
Discount for maturity 2019-08-30: 2.1007142857142855
Discount for maturity 2019-08-31: 2.1017857142857141
Discount for maturity 2019-09-01: 2.1028571428571428
...
```

## Data Source
[Treasury Site](https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=billrates)


## Contact Us
Fluidity is a financial technology company based in Brooklyn, New York, on a mission to rebuild finance using blockchain technology. Reach us at team@fluidity.io for any inquiries related to this repository, the Tokenized Asset Portfolio (TAP), or working with our team.
