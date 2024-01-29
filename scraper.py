from bs4 import BeautifulSoup


def scraper(response):
    data_list = list()
    data = {}
    soup = BeautifulSoup(response, 'html.parser')
    try:
        data["profile_name"]=soup.find("div",{"class":"r-1vr29t4"}).text
    except:
        data["profile_name"]=None
    try:
        data["profile_handle"]=soup.find("div",{"class":"r-1wvb978"}).text
    except:
        data["profile_handle"]=None
    try:
        data["profile_bio"]=soup.find("div",{"data-testid":"UserDescription"}).text
    except:
        data["profile_bio"]=None
    profile_header = soup.find("div",{"data-testid":"UserProfileHeader_Items"})
    try:
        data["profile_category"]=profile_header.find("span",{"data-testid":"UserProfessionalCategory"}).text
    except:
        data["profile_category"]=None
    try:
        data["profile_website"]=profile_header.find('a').get('href')
    except:
        data["profile_website"]=None
    try:
        data["profile_joining_date"]=profile_header.find("span",{"data-testid":"UserJoinDate"}).text
    except:
        data["profile_joining_date"]=None
    try:
        data["profile_following"]=soup.find_all("a",{"class":"r-rjixqe"})[0].text
    except:
        data["profile_following"]=None
    try:
        data["profile_followers"]=soup.find_all("a",{"class":"r-rjixqe"})[1].text
    except:
        data["profile_followers"]=None
    data_list.append(data)
    print(data_list)