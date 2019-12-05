import urllib.request
from bs4 import BeautifulSoup
import re

count=1
for i in range(1,6):

    url = "https://store.musinsa.com/app/styles/lists?sex=&use_yn_360=&brand=&model=&max_rt=2019&min_rt=2010&year_date=2016&month_date=&display_cnt=60&list_kind=small&sort=rt&page="+str(i)
    req = urllib.request.Request(url)
    res = urllib.request.urlopen(url).read()
    
    soup = BeautifulSoup(res,'html.parser')
    imagelinks = soup.findAll("div",class_="list_img opacity_img")
    
    for imagelink in imagelinks:
        imageName= imagelink.find("img").get("alt")
        s = imagelink.find("a").get('onclick')
        
        s = int(re.findall('\d+', s)[0])
        '''
        newURL = "https://store.musinsa.com/app/styles/views/"+str(s)+"?sex=&use_yn_360=&brand=&model=&max_rt=2019&min_rt=2010&year_date=2019&month_date=&display_cnt=60&list_kind=small&sort=rt&page="+str(i)

        req = urllib.request.Request(newURL)
        res = urllib.request.urlopen(newURL).read()
        image = BeautifulSoup(res,'html.parser')
        imageUrl = image.findAll("img",class_="detail_img slick-slide slick-current slick-active").get("src")
        imageName = image.find("img",class_="detail_img slick-slide slick-current slick-active").get("alt")
        if imageUrl != None:
            urllib.request.urlretrieve("https:"+imageUrl, './newimage/'+imageName.replace('?','')+'.jpg')
        '''

        newURL="http://image.msscdn.net//images/style/detail/"+str(s)+"/detail_"+str(s)+"_1_500.jpg"
        #urllib.request.urlretrieve(newURL, './newimage/'+imageName.replace('?','')+'.jpg')
        urllib.request.urlretrieve(newURL, './/MSS-2016//'+str(count)+'.jpg')
        count+=1
