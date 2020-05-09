#! /Users/stephenlang/anaconda/bin/python
#downloadXkcd.py - Downloads every single XKCD comic.

import os, requests, bs4, logging

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s -  %(levelname)s-  %(message)s')
logging.debug('Start of program')

url = 'http://xkcd.com' 
os.makedirs('xkcd',exist_ok=True)
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

while not url.endswith('#'):
    #Download the page
    print('Downloading page %s...' % url)
    res = requests.get(url, headers=headers)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    #Find the url of the comic image
    comicElem = soup.select('#comic img')
    logging.debug(comicElem)
    if comicElem == []:
       print('Could not find image')
    else:
        comicUrl = 'http:' + comicElem[0].get('src')
        logging.debug(comicUrl)
        #Download the image
        print('Downloading image %s' % comicUrl)
        res = requests.get(comicUrl,headers=headers)
        res.raise_for_status()

    #save the image to xkcd
    imageFile = open(os.path.join('xkcd',os.path.basename(comicUrl)),'wb')
    logging.debug(imageFile)
    for chunk in res.iter_content(100000):
        imageFile.write(chunk)
    imageFile.close()

    #Get the Prev button's url
    prevLink = soup.select('a[rel="prev"]')[0]
    url = 'http://xkcd.com' + prevLink.get('href')
print('Done')
logging.debug('End of program')