import csv
import json
import requests
import sys
import urllib.request

from bs4 import BeautifulSoup

def get_soup(url,header):
    return BeautifulSoup(urllib.request.urlopen(
        urllib.request.Request(url,headers=header)),
        'html.parser')

def bing_search(query):
    query= query.split()
    query='+'.join(query)
    url="http://www.bing.com/images/search?q=" + query + "&FORM=HDRSC2"

    header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    soup = get_soup(url,header)
    image_result_raw = soup.find("a",{"class":"iusc"})

    m = json.loads(image_result_raw["m"])
    url = m["turl"]

    return url

def get_logo_and_fav(website):

    fav_url = ''
    logo_url = ''
    url = f'http://www.{website}'
    print(url)
    html = requests.get(url, timeout=6, allow_redirects=True)
    actual_link=html.url #We have it in case we are redirected
    print(html)
    soup = BeautifulSoup(html.text, 'lxml')
    fav_attributes = [
        'icon', 'shortcut icon', 'apple-touch-icon', 'apple-touch-icon-precomposed', 'apple-touch-startup-image',
        'mask-icon', 'fluid-icon'
    ]
    favicon_tags = soup.findAll('link', {'rel': fav_attributes})
    fav_extensions = [
        ".jpg", ".png", ".gif", ".tif", ".svg", ".ico", ".bmp"
    ]


    for link in favicon_tags:
        possible_url = link.get('href')
        if any(x in possible_url for x in fav_extensions):
            fav_url = possible_url
            break

    if fav_url == '': 
        fav_url = f'{actual_link}favicon.ico'
        # In case it's not found, we write the favicon default URL for most websites

    if fav_url != '' and 'http' not in fav_url:
        fav_url = f'{actual_link}{fav_url}' 
        #Sometimes, we don't get the absolute path,
        # so we have to build it

    logo_tags = soup.select(':is(img, svg)[src*="logo"]')
    for link in logo_tags:
        possible_url = link.get('src',"")
        if 'logo' in possible_url:
            logo_url = possible_url
            break

    if logo_url != '' and 'http' not in logo_url:
        logo_url = f'{actual_link}{logo_url}' 
        #Sometimes, we don't get the absolute path,
        # so we have to build it

    if logo_url == '':
        company = actual_link.split('.')[1]
        query = f'{company} logo'
        logo_url=bing_search(query)
        #In case the logo is not found, we use Bing Search Engine
        #to scrape the logo, which is accurate most of the times

    
    return logo_url, fav_url

def main():
    """
    We should like run the program like this: python3 main.py < path/file.csv
    so that it reads CSV file from STDIN
    """
    data = sys.stdin.read()
    websites = data.split('\n')
    with open('../../results.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['website', 'logo_url', 'fav_url'])
        for website in websites:
            try:
                print(website, type(website))
                logo_url, fav_url = get_logo_and_fav(website)
                writer.writerow([website, logo_url, fav_url])
            except Exception as ex:
                error = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = error.format(type(ex).__name__, ex.args)
                print(message)
                writer.writerow([website, type(ex).__name__,type(ex).__name__])
                #In case there's an exception, we fill the row with the website and the name of the exception 

if __name__ == "__main__":
    main()

