from lxml import html
import requests


def write_row(lyst):
    for i, data in enumerate(lyst):
        f.write(data)
        if i+1 != len(lyst):
            f.write(',')
    f.write('\n')

f = open('output.csv', 'w')
page = requests.get('http://data.investmentnews.com/aotm/')
tree = html.fromstring(page.text)
xquery = tree.xpath('//table[@class="dataTable display treeTable rwd-table"]')
table_headers = xquery[0].xpath('thead//a/text()')
table_rows = xquery[0].xpath('tbody/tr')
write_row(table_headers)
for row in table_rows:
    row_data = row.xpath('td/text()')
    row_data.insert(0, '"' + row[0][0].text + '"')
    write_row(row_data)
    print row_data
f.close()
