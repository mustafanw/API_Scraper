import requests
from bs4 import BeautifulSoup
import pandas as pd
url= "https://www.programmableweb.com/apis/directory"
#url='https://www.programmableweb.com/apis/directory?page=748'

response = requests.get(url)
data = response.text
soup=BeautifulSoup(data,"html.parser")
apisodd=soup.find_all('tr',{'class':'odd'})
apiseven=soup.find_all('tr',{'class':'odd'})
api_no=0
dict_api={}
while True:
    for api in apisodd:
        apiname=api.find('a').text
        apiurl = 'https://www.programmableweb.com'+ api.find('a').get('href')
        apidesc_tag = api.find('td',{'class':'views-field views-field-search-api-excerpt views-field-field-api-description hidden-xs visible-md visible-sm col-md-8'})
        apidesc= apidesc_tag.text.strip() if apidesc_tag else "NA"
        apicat_tag = api.find('td', {'class': 'views-field views-field-field-article-primary-category'})
        apicat=apicat_tag.text.strip() if apicat_tag else "NA"
        api_no+=1
        print(api_no)
        dict_api[api_no]=[apiname,apiurl,apicat,apidesc]
    for api in apiseven:
        apiname=api.find('a').text
        apiurl = 'https://www.programmableweb.com'+ api.find('a').get('href')
        apidesc_tag = api.find('td', {'class': 'views-field views-field-search-api-excerpt views-field-field-api-description hidden-xs visible-md visible-sm col-md-8'})
        apidesc = apidesc_tag.text.strip() if apidesc_tag else "NA"
        apicat_tag = api.find('td', {'class': 'views-field views-field-field-article-primary-category'})
        apicat = apicat_tag.text.strip() if apicat_tag else "NA"
        api_no+=1
        print(api_no)
        dict_api[api_no]=[apiname,apiurl,apicat,apidesc]

    #nextpage=soup.find('li',{'class':'pager-last'}).find('a')
    if soup.find('li',{'class':'pager-last'}):
        nextpage = soup.find('li', {'class': 'pager-last'}).find('a').get('href')
        response = requests.get('https://www.programmableweb.com'+nextpage)
        #print('https://www.programmableweb.com'+nextpage.get('href'))
        data=response.text
        soup=BeautifulSoup(data,'html.parser')
        apisodd = soup.find_all('tr', {'class': 'odd'})
        apiseven = soup.find_all('tr', {'class': 'odd'})
    else:
        break


api_df=pd.DataFrame.from_dict(dict_api,orient='index',
                              columns=['Name','URL','Category','Description'])

api_df.to_csv('all_api.csv')