from selenium import webdriver
from datetime import datetime

driver=webdriver.Edge(r"C:\Users\hhrh1\Desktop\edgedriver_win64\msedgedriver.exe")

bankuai_links=["https://www.mysmth.net/nForum/#!section/9", "https://www.mysmth.net/nForum/#!section/7"]

number_of_tiezi=10

interval=datetime.timedelta(hours=5)

# returns current date and time
now = datetime.now()

earliest_date= now-interval

#the number of hottest tiezis that you want to display
k=10

"""
Firstly visit each bankuai link, collect the links of all banmian links in that bankuai.
Then visit each banmian link, collect the links of all tiezi that should be explored in that banmian
Then visit each tiezi, count the follow-ups of which the date is later than the allowed earliest date.
Define a list recording top 10 hotest tiezis' links and number of recent follow-ups, and maintain it during counting.
If a tiezi's total folow-ups are fewer than the 10th hottest tiezi's recent follow-ups, then there is no need to count its recent follow-ups.
Visit the tiezi's link, and count its recent follow-ups.
If its recent follow-ups are more than the 10th hottest tiezi's, update the list.
Display the links of with top 10 hottest tiezis.
"""


#initialize the list with count=0 and null string links
top_k_hottest_tiezi=[]
cnt=0
while cnt<k:
    top_k_hottest_tiezi.append([0,""])

for bankuai_link in bankuai_links:
    # get source code
    driver.get(bankuai_link)

    """
    html = driver.page_source
    time.sleep(2)

    with open("C:\\Users\\hhrh1\\Desktop\\HTML.txt", "w",encoding='utf-8') as o:
        o.write(html)
    """

    tbody = driver.find_elements_by_tag_name("tbody")
    tbody = tbody[0]
    td_list = tbody.find_elements_by_class_name("title_1")

    banmian_links = []
    for td in td_list:
        a = td.find_elements_by_tag_name("a")
        banmian_links.append(a[0].get_attribute("href"))

    # get the links of every tiezi that has at least one follow-up that is later than the allowed earliest date
    tiezi_links = []
    for banmian_link in banmian_links:
        driver.get(banmian_link)
        tbody = driver.find_elements_by_tag_name("tbody")
        tbody = tbody[0]
        tr_list=tbody.find_elements_by_tag_name("tr")

        # remove top tds
        tr_list_top = tbody.find_elements_by_class_name("top")
        number_of_top = len(tr_list_top)
        tr_list=tr_list[number_of_top:-1]

        for tr in tr_list:
            #if the latest tiezi is older than that allowed by the defined interval, then there is no need to continue the loop
            tmp_td_list=tr.find_elements_by_class_name("title_10")
            if len(tmp_td_list)==0:
                tmp_td_list = tr.find_elements_by_class_name("title_10 bg-odd")

            latest_date_list=tmp_td_list[1].find_elements_by_tag_name("a").get_attribute("text").split("-")
            latest_date = datetime.date(latest_date_list[0], latest_date_list[1], latest_date_list[2])
            if earliest_date>latest_date_list:
                break

            #if the total follow-ups are fewer than the recent follow-ups of the 10th hotest tiezi,
            # then there is no need to count this tiezi's recent follow-up.
            tmp_td_list = tr.find_elements_by_class_name("title_11 middle")
            if len(tmp_td_list)==0:
                tmp_td_list = tr.find_elements_by_class_name("title__11 middle bg-odd")
            number_of_follow_ups=int(tmp_td_list[2].get_attribute("text"))
            if number_of_top<top_k_hottest_tiezi[k-1][0]
                continue

            tmp_td_list=tr.find_elements_by_class_name("title_9")
            if len(tmp_td_list)==0:
                tmp_td_list = tr.find_elements_by_class_name("title_9 bg-odd")

            a = tmp_td_list[0].find_elements_by_tag_name("a")
            tiezi_links.append(a[0].get_attribute("href"))

        tiezi_links=[]
        for td in td_list:
            a = td.find_elements_by_tag_name("a")
            tiezi_links.append(a[0].get_attribute("href"))

        for tiezi_link in tiezi_links:
            driver.get(tiezi_link)
            td_list=driver.find_elements_by_class_name("a-content")
            #extract the follow-ups
            td_list=td_list[1:-1]
            #the follow-ups are listed in the time-ascending order, so we iterate it backwards
            for td in reversed(td_list):
                p=td.find_elements_by_tag_name("p")
                text=p.get_attribute("text")
                #extract the date from the text
                #the date follows the words "水木社区"
                date=text.find()













# close web browser
driver.close()
