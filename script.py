from bs4 import BeautifulSoup
import datetime
from random import randint
from random import shuffle
import requests
from time import sleep

def get_html(url):
    
    html_content = ''
    try:
        page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_content = BeautifulSoup(page.content, "html.parser")
    except: 
        pass
    
    return html_content

def get_value(html, info_name):
    
    info_value = None
    
    
    try:
        info_value = html.select('.itemDetailBtn')[0].get(info_name);
    except:
        pass
    
    return info_value 

def get_details(html):
    
    stamp = {}
    
    desc = get_value(html, 'data-desc')
    stamp['scott_num'] = get_value(html, 'data-scott')   
    
    price = get_value(html, 'data-price') 
    price = price.replace('$', '')
    stamp['price'] = price  
    
    try:
        title_parts = desc.split('<br>')
        title = title_parts[0].strip()
    except:
        title = None
    
    stamp['title'] = title
    
    desc = desc.replace('<br>', '').replace('\r\n', '').strip()
    stamp['raw_text'] = desc
       
    stamp['currency'] = 'USD'
    
    # image_urls should be a list
    images = []     
    try:
        img = 'http://nalbandstamp.com/' + get_value(html, 'data-img')
        images.append(img)        
    except:
        pass

    stamp['image_urls'] = images 

    if stamp['raw_text'] == None and stamp['title'] != None:
        stamp['raw_text'] = stamp['title']
        
    # scrape date in format YYYY-MM-DD
    scrape_date = datetime.date.today().strftime('%Y-%m-%d')
    stamp['scrape_date'] = scrape_date
    
    print(stamp)
    print('+++++++++++++')
    sleep(randint(25, 65))
           
    return stamp

def get_page_items(url):

    items = []
    next_url = ''

    try:
        html = get_html(url)
    except:
        return items, next_url

    try:
        for item in html.select('.panel-footer'):
            if item not in items:
                items.append(item)
    except:
        pass
    
    try:
        next_items = html.select('.pagination a')
        for next_item in next_items:
            next_text = next_item.get_text().strip()
            next_href = next_item.get('href')
            if((next_text == '»') and (next_href != 'javascript:void(0)')):
                 next_url = 'http://nalbandstamp.com' + next_href
    except:
        pass   
    
    shuffle(list(set(items)))
    
    return items, next_url

item_dict = {
"Choice Quality": "http://nalbandstamp.com/search-for-stamps.cfm?id=90000000&subid=0",
"Mint": "http://nalbandstamp.com/search-for-stamps.cfm?id=90000000&subid=1",
"Used": "http://nalbandstamp.com/search-for-stamps.cfm?id=90000000&subid=2",
"Plate Blocks": "http://nalbandstamp.com/search-for-stamps.cfm?id=90000000&subid=3",
"Error Rarities": "http://nalbandstamp.com/search-for-stamps.cfm?id=90000000&subid=4",
"Proof/Essay": "http://nalbandstamp.com/search-for-stamps.cfm?id=90000000&subid=16",
"Colour Varieties": "http://nalbandstamp.com/search-for-stamps.cfm?id=90000000&subid=5",
"Perf Varieties": "http://nalbandstamp.com/search-for-stamps.cfm?id=90000000&subid=6",
"Canada": "http://nalbandstamp.com/search-for-stamps.cfm?id=57600000&subid=7",
"British": "http://nalbandstamp.com/search-for-stamps.cfm?id=57600000&subid=8",
"General Foreign": "http://nalbandstamp.com/search-for-stamps.cfm?id=57600000&subid=9",
"Lots and Collections": "http://nalbandstamp.com/search-for-stamps.cfm?id=57600000&subid=11",
"Commemorative Coins": "http://nalbandstamp.com/search-for-stamps.cfm?id=9999&subid=14",
"Definitive Coins": "http://nalbandstamp.com/search-for-stamps.cfm?id=9999&subid=15",
"Gold Coins": "http://nalbandstamp.com/search-for-stamps.cfm?id=9999&subid=13",
    }
    
for key in item_dict:
    print(key + ': ' + item_dict[key])   

selection = input('Choose category: ')
            
category_url = item_dict[selection]
page_url = category_url
while(page_url):
    page_items, page_url = get_page_items(page_url)
    for page_item in page_items:
        stamp = get_details(page_item)
