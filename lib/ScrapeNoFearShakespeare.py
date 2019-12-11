# import libraries
from bs4 import BeautifulSoup
import requests
import time

# define string constants
strWorkHeader = '''<html>
<link rel="stylesheet" href="https://www.sparknotes.com/vendor/stylesheets/owl.carousel.min.css">
<link href="https://fonts.googleapis.com/css?family=Raleway:100,100i,200,200i,300,300i,400,400i,500,500i,600,600i,700,700i,800,800i,900,900i" rel="stylesheet">
<link rel="stylesheet" href="https://www.sparknotes.com/build/stylesheets/styles.css?rev=1120">
<table border="0" cellpadding="0" class="noFear noFear--hasNumbers">'''
strActScenePrefix = '''<tr>
<td colspan="2">
<h1 style="text-align:center">
'''
strActSceneSuffix = '''
</h1>
<td>
</tr>'''

# define singl-page-scraping function
def ScrapePage(soup):
    lstActScene = soup.find('h2', class_='interior__page__title')
    lstTblRow = soup.find('table', class_='noFear')
    # define strings to return current Act&Scene, Lines, and counting var
    strActScene = ''
    strLines = ''
    intN = 0
    if lstActScene != None:
        strActScene = lstActScene.text
        for tr in lstTblRow:
            if intN > 1:
                strLines = f'{strLines}{tr}'
            intN += 1
    return strActScene, strLines

# scrape each all pages below root
def ScrapeWork(strFile, strURLRoot, intStartPgNum, intStep, intStartActScene):
    # update status
    print(f'scraping {strFile} . . . ')
    # set initial page number (typically 0) and act&scene (typically 'Act 1 Scene 1')
    intPgNum = intStartPgNum
    strPrevActScene = ''
    strCurrActScene = intStartActScene
    # set html for "page zero" (header html)
    strPage = strWorkHeader
    # create output file. write in append and byte (not string) format
    f = open(strFile, 'ab')
    # if page was scraped, write to file
    while strPage != '':
        # write new Act and/or Scene to page, across cols
        if strPrevActScene != strCurrActScene:
            f.write(bytes(strActScenePrefix + strCurrActScene + strActSceneSuffix, 'utf-8'))
            strPrevActScene = strCurrActScene
        # write latest page (in byte format) to file
        strPage = strPage.encode(encoding='utf-8', errors='ignore')
        f.write(strPage)
        # set increment (typically 2) and URL for next page
        intPgNum += intStep
        strURL = strURLRoot + str(intPgNum)
        # update status
        print(f'scraping {strURL} . . . ')
        # retrieve page with the requests module
        resp = requests.get(strURL)
        # create BeautifulSoup object; parse with 'lxml'
        soup = BeautifulSoup(resp.text, 'lxml')
        strCurrActScene, strPage = ScrapePage(soup)
        # replace whitespace & bad chars in strActScene & strPage
        strCurrActScene = strCurrActScene.strip()
        # wait 5 sec in compliance with robots.txt
        time.sleep(5)
    # close up the file
    f.write(bytes('''</table>
            </html>''', 'utf-8'))
    f.close()