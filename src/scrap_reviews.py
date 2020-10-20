import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

#amazon base url
base_url = "https://www.amazon.in"

#seach url to search mobile phones
search_url = "https://www.amazon.in/s?k="

# insert request cookies within{}
cookie={} 

header={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}

#list of mobiles
mobile_phones = ['redmi note 9',
                 'oneplus 7t pro',
                 'nokia 5.3',
                 'Samsung Galaxy M21',
                 'Apple iPhone 11',
                 'Apple iPhone XR',
                 'Redmi 8A',
                 'OPPO A5',
                 'OnePlus 8',
                 'Samsung S10'
                 ]


phone_links = [] #store all the links of phones in list

#scrap links for the phones
for phone in mobile_phones:
    query = '+'.join(phone.split())
    #combine serach url and search query 
    url = search_url+query
    search_response = requests.get(url,cookies= cookie,headers=header)
    soup = bs(search_response.text,'lxml')
    links = soup.findAll("a",class_="a-link-normal s-no-outline")
    phone_links.append(base_url+links[4]["href"])


def searchQuery(review_link):
    """
    input : link to search for a review 
    output : response for the link
    """
    page=requests.get(review_link,cookies=cookie,headers=header)
    if page.status_code==200:
        return page
    else:
        return "Error"
    

for j in range(len(phone_links)):
    print(f'Scraping Review for {mobile_phones[j]} ...')
    reviews = [] #list to store reviews
    page_no = 0 #intialise page number

    
    response=requests.get(phone_links[j],cookies=cookie,headers=header)
    soup=bs(response.content)
    review_link = soup.findAll("a",{'data-hook':"see-all-reviews-link-foot"})[0]['href']
    
    while(True):
        
        url = base_url+review_link+'&pageNumber='+str(page_no)
        response = requests.get(url,cookies=cookie,headers=header)
        soup=bs(response.content)
        review_block = soup.findAll("span",{'data-hook':"review-body"})

        #if no more reviews then exit from the loop
        if review_block == []:
          break
        else :
          for review in review_block:
              text = review.text 
              reviews.append(text)
        page_no = page_no+1
    print()
    
    #save the review as csv file
    df = pd.DataFrame({'review':reviews})
    phone = mobile_phones[j] + '_review.csv'
    df.to_csv("../reviews"+phone,index=False)
            
            
