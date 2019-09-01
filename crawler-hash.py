import os
import hashlib
import requests
import smtplib
from email.message import EmailMessage
import time


def get_hash(url):  # OPENS A WEBSITE AND GETS THE HASH
    request = requests.get(url)  # GET SITE
    hash = hashlib.sha256(request.text.encode(
        'utf-8'))  # GET HASH
    return hash.hexdigest() # RETURN HASH

def check_hash(site_name, temp_hash): # COMPARE NEW HASH AND STORED HASH
    try: # CHECK FOR HASH FILE
        with open(str(site_name[7:site_name.index(".")]) + ".txt", 'r') as sn: # OPEN FILE
            stored_hash = sn.read() # READ FILE
            if str(stored_hash) == str(temp_hash): # COMPARE HASHES - SAME HASH
                print(site_name + " : Same hash - NO CHANGES.")
                return False
            elif str(stored_hash != temp_hash): #COMPARE HASHES - DIFFERENT HASH - WRITE NEW HASH TO FILE
                with open(str(site_name[7:site_name.index(".")]) + ".txt", 'w') as nh: # OPEN NEW FILE IN WRITE
                    nh.write(temp_hash) # SAVE NEW HASH IN FILE
                    print(site_name + " : Different hash - writing to database... - CHANGES! ")
                    return True
    except FileNotFoundError: # NEW WEBSITE ADDED TO SITES.TXT - CREATES A HASH FILE
        with open(str(site_name[7:site_name.index(".")]) + ".txt", 'w+', ) as nh: # CREATE NEW FILE
            nh.write(temp_hash) # STORE HASH
            print(site_name + ' : New site - creating database file.')

def crawl(site_list): # CRAWL SITES
    result = [] # OUTPUT
    for site in site_list: # LOOP THROUGH SITES
        new_hash = get_hash(site) # COMPATE HASHES
        if check_hash(site, new_hash) == True: # IF WEBSITE CHANGES - WRITE TO EMAIL
            result.append("Update: " + site) # WRITE TO EMAIL
    return result

sites = []

with open('sites.txt', 'r') as s: # GET SITE LIST
    sites = s.readlines()

while True: # CRAWL SITES
    print('Crawling...')
    temp_msg = crawl(sites)

    if len(temp_msg) != 0: # CHANGES - SEND MAIL!
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.environ.get('IGOR_MAIL'), os.environ.get('IGOR_PASS'))

            msg = EmailMessage()
            msg['Subject'] = 'CHANGES!'
            msg['From'] = 'NAME_IGOR'
            msg['To'] = 'RECIVER'
            msg.set_content(str(temp_msg))

            smtp.send_message(msg)

    print("Waiting for another run.") # COOLDOWN
    time.sleep(1800)










