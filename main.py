import requests
import random
from bs4 import BeautifulSoup
import traceback
import pandas as pd


# def SaveInFile(content,path):
#     with open(path,"w",encoding="utf-8") as f:
#         f.write(content)

def getWatches(soup):
    watches = soup.find_all("div", attrs={"class":'a-section a-spacing-base a-text-center'})
    return watches
def getBrands(soup):
    brands = soup.find_all("span", attrs={"class":'a-size-base-plus a-color-base'})
    return brands
def getDescription(soup):
    descriptions = soup.find_all("span", attrs={"class":'a-size-base-plus a-color-base a-text-normal'})
    return descriptions
def getPrices(soup):
    prices = soup.find_all("span", attrs={"class":'a-price-whole'})
    return prices
def getReviews(soup):
    try:
        reviews = soup.find_all("span", attrs={"class":'a-size-base s-underline-text'})
        if reviews:
            return reviews[0].string
        else:
            return None
    except Exception as e:
        print(f"Error in getRatings: {e}")
        return None



def getRatings(soup):
    try:
        # Find the first <a> element with the specified class
        rating_link = soup.find("a", class_="a-popover-trigger a-declarative")

        if rating_link:
            # Find the <span> element with the rating text inside the <a> element
            rating_span = rating_link.find("span", class_="a-icon-alt")

            if rating_span:
                # Extract the rating text from the <span> element
                rating = rating_span.text.strip()
                return rating
            else:
                return None  # Rating span not found
        else:
            return None  # Rating link not found
    except Exception as e:
        print(f"Error in getRatings: {e}")
        return None





# url = "https://www.flipkart.com/search?q=watches%20for%20men&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
url = "https://www.amazon.in/s?k=watches+for+men&crid=3SSUV1D8CGSO2&sprefix=Watch%2Caps%2C373&ref=nb_sb_ss_ts-doa-p_2_5"
headers = {"User-Agent": "Mozilla/5.0", "accept-language": "en-US,en"}


response = requests.get(url,headers=headers)
# print(response)
# SaveInFile(response.text,'data/amazonScrap.html')


data={'Brand':[],'Description':[],"Price":[],"Ratings":[],"Reviews":[]}


with open('data/amazonScrap.html',"r",encoding="utf-8") as f:
    html_doc=f.read()

# soup=BeautifulSoup(html_doc,'html.parser')
soup=BeautifulSoup(response.text,'html.parser')

watches=getWatches(soup)

brands=[]
descriptions=[]
prices=[]
ratings=[]
reviews=[]
for watch in watches:
    brands.append(getBrands(watch)[0].string)
    descriptions.append(getDescription(watch)[0].string)
    prices.append(getPrices(watch)[0].string)
    reviews.append(getReviews(watch))
    ratings.append(getRatings(watch))


for review in reviews:
    data["Reviews"].append(review)
for desc in descriptions:
    data["Description"].append(desc)
for brand in brands:
    data['Brand'].append(brand)
for rating in ratings:
    data['Ratings'].append(rating)
for price in prices:
    data['Price'].append(price)


df=pd.DataFrame.from_dict(data)
df.to_excel("data.xlsx",index=False)
df.to_csv("data.csv",index=False)

