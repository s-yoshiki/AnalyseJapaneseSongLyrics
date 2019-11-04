from lib import utanet
from urllib.parse import quote_plus
from pprint import pprint

if __name__ == "__main__":
    keyword = quote_plus("B'z", encoding='utf-8')
    lists = utanet.search_artists(keyword)
    seq = 0
    csv_row = [
        'artist',
        'title',
        'composer',
        'lyricist',
        'lyrics',
        'date',
        'access_count',
    ]
    print('"' + '","'.join(csv_row) + '"')
    for row in lists:
        seq += 1
        data = utanet.get_lyrics_by_artistid(row['song_id'])
        csv_row = [
            data['artist'],
            data['title'],
            data['composer'],
            data['lyricist'],
            data['lyrics'],
            data['date'],
            data['access_count'],
        ]
        print('"' + '","'.join(csv_row) + '"')
