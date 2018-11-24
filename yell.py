##Wedding photographers in Liverpool with reviwed content

import requests
from lxml import html
import itertools
import sqlite3


def getphotographerlinks():
    url = "https://www.yell.com/ucs/UcsSearchAction.do?location=Liverpool&keywords=Wedding+Photographers&scrambleSeed=734099646&filter=1"
    header = {'user-agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'}
    conn = sqlite3.connect("D:\\nutan\\web scraping\\Yell.com\\yell.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE wedding_photographers (name text,website text,phone text,address text,locality text,postalcode text)''')

    for page in itertools.count():
        param = {'pageNum':page+1}
        response = requests.get(url,headers=header,params=param)
        doc = html.fromstring(response.text)
        if len(doc.xpath('//*[@id="content"]')) != 0:
               for record in doc.xpath('//*[@id="rightNav"]/div/div/article'):
                    if record.xpath('div/div[2]/div[2]/div/a/text()')[0].strip() == "Wedding Photographers":
                        name = record.xpath('div/div[2]/div[1]/div/a/h2/text()')[0].strip()
                        try:
                            website = record.xpath('div/div[2]/div[3]/div/a[@class="businessCapsule--ctaItem"]/@href')[0].strip()
                        except:
                            website = ""
                        try:
                            phone = record.xpath('div/div[2]/div[3]/div/div/div/div/span[@class="business--telephoneNumber"]/text()')[0].strip()
                        except:
                            phone = ""
                        try:
                            address = record.xpath('div/div[2]/div[4]/a/span[2]/span[@itemprop="streetAddress"]/text()')[0].strip().rstrip(',')
                        except:
                            address = ""
                        try:
                            locality = record.xpath('div/div[2]/div[4]/a/span[2]/span[@itemprop="addressLocality"]/text()')[0].strip().rstrip(',')
                        except:
                            locality = ""
                        try:
                            postalcode = record.xpath('div/div[2]/div[4]/a/span[2]/span[@itemprop="postalCode"]/text()')[0].strip()
                        except:
                            postalcode = ""
                        print(name,"----",website,"----",phone,"----",address,"----",locality,"----",postalcode)
                        c.execute("INSERT INTO wedding_photographers VALUES (?,?,?,?,?,?)",(name,website,phone,address,locality,postalcode))
        else:           
            break
    conn.commit()
    conn.close()
            
getphotographerlinks()
