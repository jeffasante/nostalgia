import urllib
from bs4 import BeautifulSoup
import re



# mobile user-agent
MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
headers={'User-Agent':MOBILE_USER_AGENT}#user_agent, } 
# headers={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"

def get(url):
    # with urllib.request.urlopen(url, headers=headers) as response:
    #     return response.read().decode('utf-8')
    request=urllib.request.Request(url,None,headers) #The assembled request
    response = urllib.request.urlopen(request)

    return (response)
        # return r


def fetchFromGoogle(title):

   

    url = 'https://google.com/search?q=' + title.replace(' ', '+')
   
    google_search_results = []

    bs = BeautifulSoup(get(url), 'html.parser')

    for link in bs.find_all('a'):
        if 'href' in link.attrs:

            # if formatted_query
            if re.search('https://en.m.wikipedia.org/wiki/', link.attrs['href']):
                # print(link.attrs['href'])
                google_search_results.append(link.attrs['href'])
            
    return google_search_results
    


def fetchFromWiki(gs : list):
    
    # if gs[0]
    print(gs)
    flag = False
    # index=0
    for i, item in enumerate(gs):
        if re.search('wikipedia', item):
            flag = True
            
            # index = 0

    if gs!=[] and flag:
        url = get(gs[0])
        bs = BeautifulSoup(url, 'html.parser')
        img_urls = []
        try:
            # fetched_img = bs.td.img['src']
            for link in bs.find_all('img'):
                if 'src' in link.attrs:
                
                    if re.search('//upload.wikimedia.org/wikipedia/en/thumb', link.attrs['src']) \
                        or re.search("//upload.wikimedia.org/wikipedia/commons/thumb/", link.attrs['src']):
                        # print(link.attrs['src'])

                        fetched_img = link.attrs['src']
                        img_urls.append(fetched_img)
                        # print(fetched_img)
            return img_urls[0]
            
        except:
            print('Image wasnt found')
    else:
        print('Image link wasnt found')





def engine(text):
    res = fetchFromGoogle(text)
    f_res = fetchFromWiki(res)

    return f_res
