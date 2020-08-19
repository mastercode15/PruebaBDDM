import requests
from bs4 import BeautifulSoup
# Import MongoClient from pymongo so we can connect to the database
from pymongo import MongoClient


if __name__ == '__main__':
    # Instantiate a client to our MongoDB instance
    db_client = MongoClient('mongodb://localhost:27017')
    bdd3 = db_client.bdd3
    imgRadios = bdd3.posts


    response=requests.get("https://radios.com.ec/")
    soup=BeautifulSoup(response.content, "lxml")

    post_titles=soup.find_all("img", class_="cover")

    extracted=[]

    for post_title in post_titles:
        extracted.append({
            'link': "radios.com.ec/" + post_title['src']
        })

    for post in extracted:
        if db_client.bdd3.imgRadios.find_one({'link': post['link']}) is None:
            # Let's print it out to verify that we added the new post
            print("Found a new listing at the following url: ", post['link'])
            db_client.bdd3.imgRadios.insert(post)
            