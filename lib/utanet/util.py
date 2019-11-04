import urllib3
import re
import certifi
from bs4 import BeautifulSoup

def request(url):
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where())
    r = http.request('GET', url)
    return BeautifulSoup(r.data, 'html.parser')

def get_pnum_from_url(url):
    def __get_num(query):
        for block in re.split('[&|?]', query):
            obj = re.split('=', block)
            if obj[0] == 'pnum':
                return obj[1]
    soup = request(url)
    el1 = soup.findAll("div", {"id":"page_list"})[0]
    pnum_max = 0
    for el2 in el1.findAll(['a']):
        url_obj = urllib3.util.parse_url(el2.get("href"))
        p = int(__get_num(url_obj.query)) 
        if pnum_max < p:
            pnum_max = p
    if pnum_max == 0:
        pnum_max = 1
    return pnum_max

def get_records(url):
    soup = request(url)
    tables = soup.findAll("table")
    row_count = 0
    records = []
    for table in tables:
        rows = table.findAll("tr")
        del rows[0]
        if (row_count > 0):
            del rows[0]
        for row in rows:
            ex_row = []
            for cell in row.findAll(['td', 'th']):
                ex_row.append(cell.get_text())
            a = row.findAll(['a'])
            song_id = a[0].get("href").split('/')[2]
            records.append({
                'song_id': song_id,
                'title': ex_row[0],
                'artist': ex_row[1],
                'lyricist': ex_row[2],
                'composer': ex_row[3],
            })
    row_count += 1
    return records

def get_detail(url):
    soup = request(url)
    result = {
        'title': '',
        'artist': '',
        'lyrics': '',
        'lyricist': '',
        'composer': '',
        'date': '',
        'access_count': '',
    }
    # title
    div = soup.findAll("h2")
    if len(div) > 0:
        result['title'] = div[0].get_text()
    # artist
    div = soup.findAll("span", {"itemprop": "byArtist name"})
    if len(div) > 0:
        result['artist'] = div[0].get_text()
    # lyrics
    div = soup.findAll("div", {"id": "kashi_area"})
    if len(div) > 0:
        text = str(div[0])
        # 改行コード置換
        text = text.replace('<br>','\n')
        text = text.replace('</br>','\n')
        text = text.replace('<br/>','\n')
        # \u3000 -> space
        text = text.replace('　',' ')
        data = BeautifulSoup(text, 'html.parser')
        result['lyrics'] = data.get_text()
    # lyricist
    div = soup.findAll("h4", {"itemprop": "lyricist"})
    if len(div) > 0:
        result['lyricist'] = div[0].get_text()
    # composer
    div = soup.findAll("h4", {"itemprop": "composer"})
    if len(div) > 0:
        result['composer'] = div[0].get_text()
    # date
    div = soup.findAll("div", {"id": "view_amazon"})
    if len(div) > 0:
        m = re.search(r'[0-9][0-9][0-9][0-9]\-[0-9][0-9]\-[0-9][0-9]', div[0].get_text().strip())
        if m != None:
            result['date'] = str(m.group())
    # access_count
    div = soup.findAll("div", {"class": "access_count"})
    if len(div) > 0:
        div2 = div[0].findAll('span')
        if len(div2) > 0:
            result['access_count'] = div2[0].get_text().replace(",", "")
    return result