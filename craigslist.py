import requests
from bs4 import BeautifulSoup
from requests.api import post
import time
import random
import pickle
import datetime

post_title_texts = []
post_links = []
post_timing = []
try:
    saved_data = open('data','rb')
    post_links_found = pickle.load(saved_data)
    saved_data.close()
    print("Previous save loaded")
except:
    post_links_found = []
    print("Empty list created")
page_num = 0
iteration = 1
search_terms = ['microwave','computer','tv','microwaves','computers','tvs','laptops','laptop','motherboards','motherboard','pc','pcs','ps1','ps2','ps3','ps4','ps5','xbox','broken','tech','technology','floppy','stuff','item','items','lot','lots']
webhookUrl = "webhook url"

while(True):
    try:
        x = requests.get("link")
        html_soup = BeautifulSoup(x.text, 'html.parser')
        results_num = html_soup.find('div', class_= 'search-legend')
        results_total = int(results_num.find('span', class_='totalcount').text) 
        total_pages = round((results_total / 120) + 0.5)
    except:
        print("Something bad happened :(")

    for i in range(0,total_pages):
        y = requests.get("link"+str(page_num)+"link")
        page_num += 120
        html_soup2 = BeautifulSoup(y.text, 'html.parser')
        posts2 = html_soup2.find_all('li', class_= 'result-row')
        for post in posts2:
            post_title = post.find('a', class_='result-title hdrlnk')
            post_title_text = post_title.text.lower()
            post_title_texts.append(post_title_text)

            post_link = post_title['href']
            post_links.append(post_link)
            
            post_datetime = post.find('time', class_= 'result-date')['datetime']
            post_timing.append(post_datetime)

    for i in range(0,len(post_title_texts)):
        if any(ext in post_title_texts[i] for ext in search_terms):
            if(post_links[i] not in post_links_found):
                post_links_found.append(post_links[i])
                date = datetime.datetime.now().date()
                post_date = post_timing[i].split()
                if(str(post_date[0]) == str(date)):
                    message = post_links[i] + " " + post_timing[i]
                    webhookData = {
                    "content" : message
                    }
                    sendWebhook = requests.post(webhookUrl, json = webhookData, timeout=1)
                    print(post_links[i])

    data = open('data','wb')
    pickle.dump(post_links_found,data)
    data.close()
    page_num = 0
    print("Iteration: " + str(iteration))
    iteration+=1
    time.sleep(random.randint(30,60))
