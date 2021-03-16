import csv
import requests
from bs4 import BeautifulSoup
import sys


def get_logo_and_fav(website):
    
    brand = website.split('.')[0]
    
    fav_url = ''
    logo_url = ''
    html=requests.get('http://www.'+ website, timeout=7,allow_redirects=True)
    soup = BeautifulSoup(html.text, 'html.parser')

    fav_attributes=['icon','shortcut icon','apple-touch-icon','apple-touch-icon-precomposed','apple-touch-startup-image','mask-icon','fluid-icon']
    
    favicon_tags = soup.findAll('link',{'rel':fav_attributes})
    
    fav_extensions=[".jpg",".png", ".gif", ".tif" , ".svg", ".ico",".bmp"]
    
    for link in favicon_tags:
        possible_url = link.get('href')
        if any(x in possible_url for x in fav_extensions) :
           fav_url = possible_url
           break
    
    if fav_url == '':
        fav_url='http://www' + website + '/favicon.ico'

    
    logo_tags=soup.select('img') 
    
    for link in logo_tags:
        possible_url= link.get('src')
        if 'logo' in possible_url:
           logo_url = possible_url
           break
        
    if logo_url!='' and 'http' not in logo_url:
        logo_url = 'http://www.'+ website + logo_url


    return logo_url,fav_url


def main():
    data = sys.stdin.read() 
    websites = data.split('\n')

    for website in websites:
        logo_URL=''
        fav_URL=''
        try:
            logo,favicon=get_logo_and_fav(website)
            with open('results.csv', 'a+') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([website, logo_url, fav_url])
                csv.close()
        except:
            print('Error')


        
if __name__=="__main__": 
    main()
