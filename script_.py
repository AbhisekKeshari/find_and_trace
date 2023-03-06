# importing libraries
import time

start = time.time()

import json
import requests
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup # BeautifulSoup is in bs4 package 

cols_str = 'phone_num,source_1_telecoms_circle_state,source_1_sim_card_distributed_at,source_2_state,source_2_service_provider,source_2_city,source_2_latitude,source_2_longitude\n'

# API discription
# find-and-trace primary source of cellular location details
URL = 'https://www.findandtrace.com/trace-mobile-number-location?mobilenumber={}&submit=Trace'
# mobilenumbertracker.com secondary source of cellular location details
URL_2 = "https://mobilenumbertracker.com/mobilenumberlocation/{}"
# use mobile phone number have 10 digits
mobile_number = '9425820438'
submit = 'Trace'

# reading phone number details
df_phone_num = pd.read_csv('./kfy_data_addition.csv')

phone_num_list = list(set(df_phone_num.phone_num.to_list()))

session_len = len(phone_num_list)

fields = ['phone_num','telecoms_circle_state','sim_card_distributed_at']
# counter_ = 0

# fetch function for getting geolocation details from phone number by source 1 and source 2
# source 1 : findandtrace
# source 2 : mobilenumbertracker.com 
def fetch(session, phone_num):
    with session.get(URL.format(phone_num)) as response:
        html = response.content.decode("utf-8")
        soup = BeautifulSoup(html, 'html.parser')
        tables = soup.find_all('table',{'class':'shop_table'})
        try:
            phone_num_ = tables[0].find_all('td')[0].text
        except:
            phone_num_ = phone_num
        try:
            telecoms_circle_state = tables[0].find_all('td')[1].text
        except:
            telecoms_circle_state = 'not_found'
        try:
            sim_card_distributed_at = tables[1].find_all('td')[0].text
            sim_card_distributed_at = (' / ').join(sim_card_distributed_at.split(', '))
        except:
            sim_card_distributed_at = 'not_found'

        resp = {
            'phone_num':phone_num_,
            'telecoms_circle_state':telecoms_circle_state,
            'sim_card_distributed_at':sim_card_distributed_at
        }
        str_ = str(phone_num_)+','+str(telecoms_circle_state)+','+str(sim_card_distributed_at)

    with session.get(URL_2.format(str(phone_num)[:4])) as response_2:
        html = response_2.content.decode("utf-8")
        soup = BeautifulSoup(html, 'html.parser')
        props = soup.find_all('script',{'id':"__NEXT_DATA__"})[0].text

        json_object = json.loads(props)
        state = json_object.get('props',{}).get('pageProps',{}).get('match',{}).get('State','not_found')
        if state == '':
            state = 'not_found'
        service_provider = json_object.get('props',{}).get('pageProps',{}).get('match',{}).get('ServiceProvider','not_found')
        if service_provider == '':
            service_provider = 'not_found'
        city = json_object.get('props',{}).get('pageProps',{}).get('match',{}).get('City','not_found')
        if city == '':
            city = 'not_found'
        latitude = json_object.get('props',{}).get('pageProps',{}).get('match',{}).get('latitude','not_found')
        if latitude == '':
            latitude = 'not_found'
        longitude = json_object.get('props',{}).get('pageProps',{}).get('match',{}).get('longitude','not_found')
        if longitude == '':
            longitude = 'not_found'
        str_ = str_+','+str(state)+','+str(service_provider)+','+str(city)+','+str(latitude)+','+str(longitude)+'\n'

    # print(str_)
    # counter_ = counter_ + 1
    try:
        with open('data_addition.csv', 'a') as file: 
            # writing data into a data addition csv file
            file.write(str_)
            file.close()
        print(str(phone_num)+' data ran successfully')
    except Exception as e:
        print("Something went wrong while saving record details")
        print(e)

# using multithreading speeding up the extraction process
with ThreadPoolExecutor(max_workers=100) as executor:
    with requests.Session() as session:
        executor.map(fetch, [session] * session_len, phone_num_list)
        executor.shutdown(wait=True)

# main()

end = time.time()

elapsed_time = end - start

print('Execution time:', elapsed_time, 'seconds')
