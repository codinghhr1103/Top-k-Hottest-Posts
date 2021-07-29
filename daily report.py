import json
import sqlite3
from urllib.request import urlopen
from bs4 import BeautifulSoup

# fetch parameters from the config file into BoardConfigs
with open(".\\config.json", "r") as f:
    config = json.load(f)

BoardConfigs = dict.fromkeys(config["BoardURLs"], config["CommonCase"])

SpecialCase = config["SpecialCase"]
cur = 0
while cur+1 < len(SpecialCase):
    BoardConfigs[SpecialCase[cur]] = SpecialCase[cur+1]
    cur += 2

# Connecting to sqlite
conn = sqlite3.connect('TopK.db')

# Creating a cursor object using the cursor() method
cursor = conn.cursor()

for BoradURL in BoardConfigs:
    list_diff = []
    response = urlopen(BoradURL)
    #html = str(response.read())
    #print(html)
    #with open("C:\\Users\\hhrh1\\Desktop\\HTML.txt", "w", encoding='utf-8') as o:
    #    o.write(html)
    soup = BeautifulSoup(response, 'html.parser')
    section = soup.html.body.contents[2].contents[1]
    print(section["id"])
    print(len(section.contents))


    for tr in tr_list:
        td_list = tr.select(".title_11 middle")
        if len(td_list) == 0:
            td_list = tr.select(".title_11 middle bg-odd")
        td = td_list[2]
        latest_cnt = int(str(td.string))

        td_list = tr.select(".title_9")
        if len(td_list) == 0:
            td_list = tr.select(".title_9 bg-odd")
        a = td_list[0].a
        relative_path = a["href"]

        cursor.execute("SELECT EXISTS(SELECT * FROM DailyReport WHERE URL=？)", (relative_path,))
        if cursor.fetchone():
            cursor.execute("SELECT cnt FROM DailyReport WHERE URL=?", (relative_path,))
            for row in cursor:
                last_cnt = row[0]
        else:
            cursor.execute("INSERT INTO DailyReport VALUES (?,?)", (relative_path, latest_cnt))
            last_cnt = latest_cnt

        diff = latest_cnt-last_cnt
        list_diff.append((diff, relative_path))

        cursor.execute("UPDATE DailyReport SET cnt=? WHERE URL=?", (latest_cnt, relative_path))

        # sort the list in descending order according to the first element, diff
        list_diff.sort(key=lambda x: x[0], reverse=True)

        TopK = BoardConfigs[BoradURL]["TopK"]
        cur = 0
        while cur < TopK:
            print("https://www.mysmth.net"+list_diff[cur][1])
            cur += 1
