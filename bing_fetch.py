from bs4 import BeautifulSoup
import re, random
## Bing query phase

from urllib.request import Request, urlopen


# mobile user-agent
MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
headers={'User-Agent':MOBILE_USER_AGENT}

def get(url):
    
    request = Request(url,None,headers) #The assembled request
    response = urlopen(request)

    return (response)
    




def bingEngine(title):
    title += ' movie poster'
    text = title.lower().replace(' ', '+') 
    count = '1' # the number of images you need
    adult = 'off' # can be set to 'moderate'


    URL='https://bing.com/images/search?q=' + text + '&count=' + count # + '&safeSearch=' + adult + '&count=' + count

    # print('\n',URL, '\n')

    hold_img = []
    bs = BeautifulSoup(get(URL), 'html.parser')

    wow = bs.find_all('a',class_='iusc')
    for i in wow:
        try:
            # print(eval(i['m'])['murl'])
            hold_img.append(eval(i['m'])['murl'])
            # print()
        except:
            pass
    
    print('for', title, '->\n', hold_img)
    print()
    # return random.choice([random.choice(hold_img), hold_img[0]])
    return hold_img[0]
    # (random.choice(t