import requests
from bs4 import BeautifulSoup as bs
import re
import csv
base_url="https://www.e-services.taipei.gov.tw/{}&start=0&pagenum=10"
res=requests.get("https://www.e-services.taipei.gov.tw/hypage.exe?HYPAGE=WelFare/content.htm&class=")
soup=bs(res.text,"lxml")
attr_urls=soup.select("li>a")
for attr_url in attr_urls:
        info_urls=[base_url.format(attr_url["href"]) for attr_url in attr_urls if attr_url["href"].startswith('hypage.exe')]


base_url1="https://www.e-services.taipei.gov.tw/{}&start={}&pagenum=10"
contents=[]
numbers=[0,1,2,3,4]
for info_url in info_urls:
        info_url=info_url.replace("content","menu")
        r=requests.get(info_url)
        soup=bs(r.text,"lxml")
        links=soup.select("li > a")       
                
        for link in links:
                
                for number in numbers:         
                        all_urls=base_url1.format(link["href"],number)
                        contents.append(all_urls)


headers=["福利名稱",'福利內容','福利取得方式']
with open('台北福利雲1.csv','w',encoding="utf-8-sig",newline="") as fp:

        writer=csv.DictWriter(fp,headers)
        data=[]
        check=[]
        for content in contents:
                r=requests.get(content)
                r.encoding="utf-8"
                soup=bs(r.content,"lxml")
                name_tag=soup.select("div",class_="content")[0]
                names=name_tag.select("h3")[0].get_text()
                info=name_tag.select("p")[1]
                infos=info.get_text()
                how_to_gets=name_tag.select("p")[3].get_text()     
                welfare={'福利名稱':names,
                "福利內容":infos,
                "福利取得方式":how_to_gets,                
                }

                if welfare.get("福利名稱") in check:
                        continue
                data.append(welfare)
                check.append(welfare.get("福利名稱"))
        writer.writerows(data)
       