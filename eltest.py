from lxml import html
import requests
from pymongo import MongoClient
import re


def get_pages():
    page = requests.get('http://data.investmentnews.com/aotm/')
    tree = html.fromstring(page.text)
    p = tree.xpath('//p[@class="search-hits-bottom center"]/text()')
    x = re.split(' ', p[0])
    y = re.split(',', x[5])
    items = int(''.join(y))
    i_per_page = int(x[3]) - int(x[1]) + 1
    return items/i_per_page


def write_row(lyst):
    xtable = {'advicers': lyst[0],
              'firm_joining': lyst[1],
              'firm_leaving': lyst[2],
              'aum': lyst[3],
              'date': lyst[4]
              }
    x_table = db.x_table
    xtable_id = x_table.inser_one(xtable).inserted_id
    print xtable_id


# Connect database here
client = MongoClient('mongodb://localhost:27017/')
db = client.eltest_db

for page in range(1, get_pages()):
    page = requests.get('http://data.investmentnews.com/aotm/' + '?PAGE=' + str(page))
    tree = html.fromstring(page.text)
    xquery = tree.xpath('//table[@class="dataTable display treeTable rwd-table"]')

    table_rows = xquery[0].xpath('tbody/tr')
    for row in table_rows:
        row_data = row.xpath('td/text()')
        advicers = re.split(',', row[0][0])
        row_data.insert(0, advicers)

        # write to database here
        write_row(row_data)
        print row_data
