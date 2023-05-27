from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd
import csv
import time

data = pd.read_csv('output.csv')
df = pd.DataFrame(data)
urls = list(df['url'])




def get_soup(URL):
    webdriver_path = "E:\chromedriver_win32\\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=webdriver_path)
    driver.get(URL)
    # time.sleep()
    soup = BeautifulSoup(driver.page_source,'html.parser')
    return soup

# urls = ["https://www.amazon.in/BennettTM-Mystic-Shoulder-Messenger-Repellent/dp/B09321GJXZ/ref=sr_1_77?keywords=bags&sr=8-77&th=1",
#         "https://www.amazon.in/Genie-Glitter-Backpack-Women-compartments/dp/B097JHQH13/ref=sr_1_20?keywords=bags&sr=8-20",
#         "https://www.amazon.in/Wesley-Milestone-Waterproof-Backpack-Business/dp/B084JGJ8PF/ref=sr_1_3?keywords=bags&sr=8-3&th=1",
#         "https://www.amazon.in/Lavie-Sport-Duffle-Luggage-Trolley/dp/B097RJ22Q3/ref=sr_1_48?keywords=bags&sr=8-48&th=1",
#         "https://www.amazon.in/sspa/click?ie=UTF8&spc=MTo0MzkyMDc1NzM1OTQ5MzUyOjE2ODUxMTcyMjY6c3BfYXRmOjIwMTE2ODc5MTczOTk4OjowOjo&url=%2FRed-Lemon-Ironlook-Briefcase-Anti-Theft%2Fdp%2FB09ZYQJHXR%2Fref%3Dsr_1_1_sspa%3Fkeywords%3Dbags%26qid%3D1685117226%26sr%3D8-1-spons%26sp_csd%3Dd2lkZ2V0TmFtZT1zcF9hdGY%26psc%3D1"]

# output  = []

# df2 = pd.DataFrame(urls,columns=['url'])

def get_asin(dom):
        try:
            asin = dom.xpath('//*[@id="detailBullets_feature_div"]/ul/li[4]/span/span[2]')[0].text.strip()
        except:
            try:
                asin = dom.xpath('//*[@id="productDetails_detailBullets_sections1"]/tbody/tr[1]/td')[0].text.strip()
            except:
                asin =""
        return asin
    
def get_manf(dom):
        try:
            manf = dom.xpath('//*[@id="detailBullets_feature_div"]/ul/li[3]/span/span[2]')[0].text.strip()
        except:
            try:
                manf = dom.xpath('//*[@id="productDetails_techSpec_section_1"]/tbody/tr[2]/td')[0].text.strip()
            except:
                manf =""
        return manf
    
def get_prod_des(dom):
     try:
            des = dom.xpath('//*[@id="productDescription"]/p/span')[0].text.strip()
     except:
            des =""
     return des
    
prod_des=[]
manfs =[]
asins = []
    
for url in urls :
    dom = etree.HTML(str(get_soup(url)))
    des = get_prod_des(dom)
    manf = get_manf(dom)
    asin= get_asin(dom)
    asins.append(asin)
    prod_des.append(des)
    manfs.append(manf)

df["ASIN"] = asins
df["Manufacturer"] = manfs
df["Product Description"] = prod_des

df.to_csv('output2.csv')
    
 