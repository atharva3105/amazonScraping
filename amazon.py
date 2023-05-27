from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import csv
import time

url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"

def get_prods(URL):
    webdriver_path = "E:\chromedriver_win32\\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=webdriver_path)
    driver.get(URL)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    prods = soup.find_all('div', {'data-component-type': 's-search-result'})
    return prods
    

def get_info(item):
    atag = item.h2.a
    try:
        name = atag.text.strip()
        pro_url = "https://www.amazon.in" +atag.get('href')
        price = item.find('span' , class_='a-price').find('span',class_='a-offscreen').text
    except:
        return
    try:
        rating = item.i.text
        num_review = item.i.find_next('span', class_='a-size-base').text                                     
    except:
        rating  = 'No Rating'
        num_review = 'No Review'
    output ={"name": name ,"url":pro_url , "price": price, "rating":rating ,'review':num_review}
    return output

def list_to_csv(data, filename):
    headers = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


final_output = []

# url = "https://www.amazon.in/s?k=bags&page=1&ref=sr_pg_2"
for x in range(1,21):
    products = get_prods(f"https://www.amazon.in/s?k=bags&page={x}&ref=sr_pg_2")
    for item in products:
        op = get_info(item)
        if op:
            final_output.append(op)
list_to_csv(final_output , filename='output.csv')

# print(final_output)



###########################PART 2####################################################################


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
 
 
 

