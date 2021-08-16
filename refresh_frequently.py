from flask import jsonify, Flask
import json
import sqlite3
from selenium import webdriver
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display

import smtplib
from email.mime.text import MIMEText

from datetime import datetime


"""
app = Flask(__name__)
@app.route('/')
"""

def dict_to_table(current_ret):
    content=""""""
    for BoardURL_ in current_ret:
        if len(current_ret[BoardURL_]) == 0:
            continue
        content += '<table style="background-color:#FFFFE0;border-collapse:collapse;color:#000;font-size:18px;">'
        content += '<caption style = "background-color:#BDB76B;color:white;width:100%;padding:5px;border:0;">' \
                   + str(BoardURL_) + '</caption>'
        # content += '<tr style = "background-color:#BDB76B;color:white;width:50%;padding:5px;border:0;“> <th>Theme</th><th>Path</th><th>Number of new follow-ups</th></tr>'

        for cur in current_ret[BoardURL_]:
            content += '<tr style="border-bottom:1px dotted #BDB76B;padding:5px;border:0;"> <td><a href="' + \
                       str(cur[1]) + '">' + str(cur[0]) + '</a></td><td>' + str(cur[2]) + '</td></tr>'
        content += '</table>'

    return content


def report_frequently():
    display = Display(visible=0, size=(800, 600))
    display.start()

    # fetch parameters from the config file into BoardConfigs
    with open("config.json", "r") as f:
        config = json.load(f)

    my_sender = 'HaoranPolarBear@163.com'

    # Connecting to sqlite
    conn = sqlite3.connect('/home/laphy/Top_K_Hottest/TopK.db')

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # ret is the dict that to be stored in the json file
    ret = dict()
    for MailAddress in config:
        # current_ret is the dict that contains the info that to be E-mailed to the current user
        current_ret = dict()

        for BoardURL in config[MailAddress]:
            threshhold = config[MailAddress][BoardURL]["ReplyCntPerInterval"]

            current_ret[BoardURL] = []

            """
            # use urlopen to get HTML
            print(BoardURL)
            resource = urlopen(BoardURL)
            page = resource.read().decode(resource.headers.get_content_charset())
            with open("C:\\Users\\hhrh1\\Desktop\\HTML.txt", "w", encoding=resource.headers.get_content_charset()) as o:
                o.write(page)
            """

            # use selenium to get HTML
            # start web browser
            driver = webdriver.Firefox()
            # get source code
            driver.get(BoardURL)
            page = driver.page_source
            # with open("C:\\Users\\hhrh1\\Desktop\\HTML_selenium.txt", "w", encoding='utf-8') as o:
            #    o.write(page)
            # close web browser
            driver.close()

            """
            # use requests.get to get HTML
            response = requests.get(BoardURL)
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
    
                cursor.execute("SELECT EXISTS(SELECT * FROM FrequentReport WHERE URL=?)", (relative_path,))
                last_cnt = 0
                if cursor.fetchone():
                    cursor.execute("SELECT cnt FROM FrequentReport WHERE URL=?", (relative_path,))
                    for row in cursor:
                        last_cnt = row[0]
                else:
                    cursor.execute("INSERT INTO FrequentReport VALUES (?,?)", (relative_path, latest_cnt))
                    last_cnt = latest_cnt
    
                diff = latest_cnt - last_cnt
                list_diff.append((diff, relative_path))
    
                cursor.execute("UPDATE FrequentReport SET cnt=? WHERE URL=?", (latest_cnt, relative_path))
    
            # sort the list in descending order according to the first element, diff
            list_diff.sort(key=lambda x: x[0], reverse=True)
    
            TopK = BoardConfigs[BoardURL]["TopK"]
            cur = 0
            while cur < TopK:
                print("https://www.mysmth.net"+list_diff[cur][1])
                cur += 1
            """
            # *******************************************************************************
            # parse HTML by beautiful soup with find() and find_all()
            soup = BeautifulSoup(page, 'html.parser')

            tbody = soup.find("html").find("body").find("section", id="main").find("section", id="body").\
                find("div",class_="b-content").find("table", class_="board-list tiz").find("tbody")

            tr_list = tbody.find_all("tr")

            print(len(tr_list))
            for tr in tr_list:

                td_list = tr.find_all(class_="title_9")
                if len(td_list) == 0:
                    td_list = tr.find_all(class_="title_9 bg-odd")
                a = td_list[0].find("a")
                relative_path = str(a["href"])
                text = str(a.string)
                print(relative_path)
                print(text)

                td_list = tr.find_all(class_="title_11 middle")
                if len(td_list) == 0:
                    td_list = tr.find_all(class_="title_11 middle bg-odd")
                # print("len(td_list): "+str(len(td_list)))
                td = td_list[2]
                latest_cnt = int(str(td.string))
                print("latest_cnt: " + str(latest_cnt))

                last_cnt = 0
                cursor.execute("SELECT cnt FROM FrequentReport WHERE URL=?", ("\'" + relative_path + "\'",))
                row = cursor.fetchone()
                if row is None:
                    cursor.execute("INSERT INTO FrequentReport (URL, cnt) VALUES (?,?)",
                                   ("\'" + relative_path + "\'", latest_cnt))
                    print("insert" + str(cursor.rowcount))
                else:
                    last_cnt = int(row[0])
                    print("select" + str(cursor.rowcount))

                print("last_cnt: " + str(last_cnt))

                diff = latest_cnt - last_cnt
                if diff >= threshhold:
                    current_ret[BoardURL].append((text, "https://www.mysmth.net" + relative_path, diff))

                cursor.execute("UPDATE FrequentReport SET cnt=? WHERE URL=?", (latest_cnt, relative_path))

            # commit once every time all posts in a boardURL is counted
            conn.commit()

        # when all boardURLs corresponding to a mail address are iterated, email the current_ret
        content = dict_to_table(current_ret)

        # email the frequent report to the registered users
        msg = MIMEText(content, 'html', 'utf-8')
        msg['From'] = my_sender
        msg['To'] = MailAddress
        msg['Subject'] = 'frequent report ' + str(datetime.now())

        server = smtplib.SMTP("smtp.163.com", 25)
        server.login(my_sender, "ZFBVVJQUIVRIVOVV")
        server.sendmail(my_sender, MailAddress, msg.as_string())
        server.quit()

        # update the ret by current_ret
        for BoardURL_ in current_ret:
            if BoardURL_ not in ret.keys():
                ret[BoardURL_] = current_ret[BoardURL_]

    conn.close()

    with open("/home/laphy/Top_K_Hottest/frequent_result.json", "w", encoding='utf-8') as o:
        json.dump(ret, o)


report_frequently()

"""
    return jsonify(ret)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
"""
