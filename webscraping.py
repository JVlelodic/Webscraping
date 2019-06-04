import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

header={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
first_url = "https://www.bimmerpost.com/page/1/?s=vs"\

url_request = requests.get(first_url, headers = header)
soup = BeautifulSoup(url_request.content, "html.parser")
last_url = soup.find_all("a",{"class":"last"})

last_num = int(last_url[0].get('href')[-8:-6])
print(last_num)
merc_num = audi_num = jag_num = lexus_num = 0

for number in range(1, last_num+1):
    num_url = "https://www.bimmerpost.com/page/" + str(number) + "/?s=vs"
    url_request = requests.get(num_url, headers = header)
    soup = BeautifulSoup(url_request.content, "html.parser")

    for division in soup.find_all("div", {"class": "arctit2"}):
        for link in division.find_all("a", href = True):
            forum = requests.get(link['href'], headers = header)
            forum_content = BeautifulSoup(forum.content, "html.parser")
            print(link['href'])

            for comments in forum_content.find_all("div", {"class": "thePostItself"}):
                merc_flag = audi_flag = lexus_flag = jag_flag = 0
                cust_comment = comments.text.lower()

                if "mercedes" in cust_comment and merc_flag != 1:
                    merc_num += 1
                    merc_flag = 1
                    print ("Current number of Mercedes' is " + str(merc_num))

                if "audi" in cust_comment and audi_flag != 1:
                    audi_num += 1
                    audi_flag = 1
                    print ("Current number of Audis' is " + str(audi_num))

                if "lexus" in cust_comment and lexus_flag != 1:
                    lexus_num += 1
                    lexus_flag = 1
                    print ("Current number of Lexus' is " + str(lexus_num))

                if "jaguar" in cust_comment and jag_flag != 1:
                    jag_num += 1
                    jag_flag = 1
                    print ("Current number of Jaguars' is " + str(jag_num))

                if jag_flag is 1 and merc_flag is 1 and audi_flag is 1 and lexus_flag is 1:
                    continue

values = [merc_num, audi_num, lexus_num, jag_num]
car_brands = ['Mercedes', 'Audi', 'Lexus', 'Jaguar']

colors = ['darkred', 'lightskyblue', 'pink', 'purple']
pie_chart,texts,autotexts  = plt.pie(values, autopct = '%.2f%%'
                                        ,colors = colors, radius= 1.5, explode = (0,0.1,0,0),
                                       textprops=dict(color='black',fontweight= 'bold',fontsize= 15))

legend = plt.legend(pie_chart, car_brands, title = "Car Brands", loc ="upper right", bbox_to_anchor=(1.5, 0.5, 0, 1),
           prop = dict(size = 12))
plt.setp(legend.get_title(), fontsize = "xx-large")
plt.show()
