from lxml import html
import requests
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
    for i, data in enumerate(lyst):
        f.write(data)
        if i+1 != len(lyst):
            f.write(',')
    f.write('\n')


# Connect database here
f = open('investmentnews.csv', 'w')

for page in range(1, get_pages()):
    page = requests.get('http://data.investmentnews.com/aotm/' + '?PAGE=' + str(page))
    tree = html.fromstring(page.text)
    xquery = tree.xpath('//table[@class="dataTable display treeTable rwd-table"]')

    table_rows = xquery[0].xpath('tbody/tr')
    table_heading = xquery[0].xpath('thead//a/text()')
    if page == 1:
        write_row(table_heading)
    for row in table_rows:
        row_data = row.xpath('td/text()')
        mod_row_data = ['"'+ x + '"' for x in row_data]
        mod_row_data.insert(0, '"' + row[0][0].text + '"')
        write_row(mod_row_data)
        print mod_row_data
f.close()
