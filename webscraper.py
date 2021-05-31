from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests

url = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/" 
browser = webdriver.Chrome("chromedriver.exe")
browser.get(url)
time.sleep(10)

def scrap():
    headers = ["NAME","LIGHT-YEARS FROM EARTH","PLANET MASS","STELLAR MAGNITUDE","DISCOVERY DATE","Hyperlink","PLANET TYPE","ORBITAL RADIUS","PLANET RADIUS","ORBITAL PERIOD","ECCENTRICITY"]
    planetdata = []
    newplanetdata = []
    for i in range(0,450):
        soup = BeautifulSoup(browser.page_source,"html.parser")
        currentpagenum = int(soup.find_all("input",attrs = {"class","page_num"})[0].get("value"))
#        if(currentpagenum < i):
#            browser.find_element_by_xpath('//*[@id="primary_column"]/div[2]/a')
        for ul_tag in soup.find_all("ul",attrs = {"class","exoplanet"}):
            li_tags = ul_tag.find_all("li")
            temp = []
            for index,li_tag in enumerate(li_tags):
                if(index == 0):
                    temp.append(li_tag.find_all("a")[0].contents[0])
                    
                else:
                    try:
                        temp.append(li_tag.contents[0])
                    except:
                        temp.append("")
        hyperlink_li_tag = li_tags[0]
        temp.append("https://exoplanets.nasa.gov/"+hyperlink_li_tag.find_all("a",href = True)[0]["href"])
            
            planetdata.append(temp)
             
        browser.find_element_by_xpath('//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[2]/a').click()
        print(f"{i} pageover")
    
    def scrapmodedata(hyperlink):
        try:
            page = requests.get(hyperlink)
            soup = BeautifulSoup(page.content,"html.parcer")
            temparray = []
            for tr_tag in soup.find_all("tr",attrs={"class":"fact_row"}):
                td_tags = tr_tag.find_all("td")
                for td_tag in td_tags:
                    try:
                        temparray.append(td_tag.find_all("div",attrs={"class":"value"})[0].contents[0])
                    except:
                        temparray.append("")
            newplanetdata.append(temparray)
        except:
            time.sleep(1)
            scrapmodedata(hyperlink)
    
    for index,data in enumerate(planetdata):
        scrapmodedata(data[5])
        print(f"{index+1}pagedone2")

    finaledata = []
    for index,data in enumerate(planetdata):
        newplanetdataelement = newplanetdata[index]
        newplanetdataelement = [elem.replace("\m","")for elem in newplanetdataelement]
        newplanetdataelement = newplanetdataelement[:7]
        finaledata.append(data+newplanetdataelement)

    with open("planets.csv","w")as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(finaledata)
        print("completed")

a = scrap()