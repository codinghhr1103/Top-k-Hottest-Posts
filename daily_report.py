from flask import jsonify, Flask
import json
import sqlite3
from selenium import webdriver
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display

app = Flask(__name__)
@app.route('/')
def report_daily():
    display = Display(visible=0, size=(800, 600))
    display.start()

    # fetch parameters from the config file into BoardConfigs
    with open("config.json", "r") as f:
        config = json.load(f)

    BoardConfigs = dict.fromkeys(config["BoardURLs"], config["CommonCase"])

    SpecialCase = config["SpecialCase"]
    cur = 0
    while cur + 1 < len(SpecialCase):
        BoardConfigs[SpecialCase[cur]] = SpecialCase[cur + 1]
        cur += 2

    # Connecting to sqlite
    conn = sqlite3.connect('/home/laphy/Top_K_Hottest/TopK.db')

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    ret = dict()
    for BoradURL in BoardConfigs:
        list_diff = []
        """
        # use urlopen to get HTML
        print(BoradURL)
        resource = urlopen(BoradURL)
        page = resource.read().decode(resource.headers.get_content_charset())
        with open("C:\\Users\\hhrh1\\Desktop\\HTML.txt", "w", encoding=resource.headers.get_content_charset()) as o:
            o.write(page)
        """

        # use selenium to get HTML
        # start web browser
        driver = webdriver.Firefox()
        # get source code
        driver.get(BoradURL)
        page = driver.page_source
        # with open("C:\\Users\\hhrh1\\Desktop\\HTML_selenium.txt", "w", encoding='utf-8') as o:
        #    o.write(page)
        # close web browser
        driver.close()

        """
        # use requests.get to get HTML
        response = requests.get(BoradURL)
        response.encoding = "gbk"
        page = response.content.decode(response.encoding)
        with open("C:\\Users\\hhrh1\\Desktop\\HTML.txt", "w", encoding="gbk") as o:
            o.write(page)
        """

        # *******************************************************************************
        """
        # parse HTML by lxml with xpath
        html = etree.HTML(page)
        tbody = html.xpath("/html/body/section/section/div[3]/table/tbody")[0]
        tr_list = tbody.xpath("//tr")
        print(len(tr_list))
        for tr in tr_list:
            td = tr.xpath("//td[7]")[0]
            latest_cnt = int(td.text)
            print(td.text)

            a = tr.xpath("//td[2]/a")[0]
            relative_path = a.get("href")
            print(relative_path)

            cursor.execute("SELECT EXISTS(SELECT * FROM DailyReport WHERE URL=?)", (relative_path,))
            last_cnt = 0
            if cursor.fetchone():
                cursor.execute("SELECT cnt FROM DailyReport WHERE URL=?", (relative_path,))
                for row in cursor:
                    last_cnt = row[0]
            else:
                cursor.execute("INSERT INTO DailyReport VALUES (?,?)", (relative_path, latest_cnt))
                last_cnt = latest_cnt

            diff = latest_cnt - last_cnt
            list_diff.append((diff, relative_path))

            cursor.execute("UPDATE DailyReport SET cnt=? WHERE URL=?", (latest_cnt, relative_path))

        # sort the list in descending order according to the first element, diff
        list_diff.sort(key=lambda x: x[0], reverse=True)

        TopK = BoardConfigs[BoradURL]["TopK"]
        cur = 0
        while cur < TopK:
            print("https://www.mysmth.net"+list_diff[cur][1])
            cur += 1
        """
        # *******************************************************************************
        # parse HTML by beautiful soup with find() and find_all()
        soup = BeautifulSoup(page, 'html.parser')

        tbody = soup.find("html").find("body").find("section", id="main").find("section", id="body").find("div",
                                                                                                          class_="b-content").find(
            "table", class_="board-list tiz").find("tbody")

        tr_list = tbody.find_all("tr")

        print(len(tr_list))
        for tr in tr_list:

            td_list = tr.find_all(class_="title_9")
            if len(td_list) == 0:
                td_list = tr.find_all(class_="title_9 bg-odd")
            a = td_list[0].find("a")
            relative_path = str(a["href"])
            print(relative_path)

            td_list = tr.find_all(class_="title_11 middle")
            if len(td_list) == 0:
                td_list = tr.find_all(class_="title_11 middle bg-odd")
            # print("len(td_list): "+str(len(td_list)))
            td = td_list[2]
            latest_cnt = int(str(td.string))
            print("latest_cnt: " + str(latest_cnt))

            last_cnt = 0
            cursor.execute("SELECT cnt FROM DailyReport WHERE URL=?", ("\'" + relative_path + "\'",))
            row = cursor.fetchone()
            if row is None:
                cursor.execute("INSERT INTO DailyReport (URL, cnt) VALUES (?,?)",
                               ("\'" + relative_path + "\'", latest_cnt))
                print("insert" + str(cursor.rowcount))
            else:
                last_cnt = int(row[0])
                print("select" + str(cursor.rowcount))

            print("last_cnt: " + str(last_cnt))

            diff = latest_cnt - last_cnt
            list_diff.append((diff, relative_path))

            cursor.execute("UPDATE DailyReport SET cnt=? WHERE URL=?", (latest_cnt, relative_path))

        # sort the list in descending order according to the first element, diff
        list_diff.sort(key=lambda x: x[0], reverse=True)

        TopK = BoardConfigs[BoradURL]["TopK"]
        cur = 0
        ret[BoradURL] = []
        while cur < TopK:
            ret[BoradURL].append("https://www.mysmth.net" + list_diff[cur][1])
            print("https://www.mysmth.net" + list_diff[cur][1])
            cur += 1

        conn.commit()
    return jsonify(ret)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')



