import urllib3
from bs4 import BeautifulSoup
from . import config

# including
from .core import search_artists
from .core import get_lyrics_by_artistid
from .core import set_http_proxy


# def search_artists(key):
#     url = config.BASE_URL + "search/?Aselect=1&Bselect=3&Keyword=%s&sort=&pnum=1" % key
#     http = urllib3.PoolManager(
#         cert_reqs='CERT_REQUIRED',
#         ca_certs=certifi.where())
#     r = http.request('GET', url)
#     soup = BeautifulSoup(r.data, 'html.parser')
#     tables = soup.findAll("table")
#     # print(len(tables[1]))
#     for table in tables:
#         rows = table.findAll("tr")
#         del rows[0]
#         del rows[0]
#         for row in rows:
#             csvRow = []
#             for cell in row.findAll(['td', 'th']):
#                 csvRow.append(cell.get_text())
#             # print(csvRow)
#             a = row.findAll(['a'])
#             print(a[0].get("href"))
#         # rows
#     return []


