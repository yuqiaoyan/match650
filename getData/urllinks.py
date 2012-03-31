import urllib
import string
from BeautifulSoup import *
import json

personURLPattern    =   re.compile(r"([/]person[/].*?)[;]")
profilesList = []


def retrieveURLSuffix(link):
#given a string find the URL that matches from /person/...;
#returns the string found
    if( len(personURLPattern.findall(str(link))) > 0 ):
        return ( personURLPattern.findall(link)[0] )
    return None

def downloadPage(URLSuffix):
#get URL page for a single person from arnetminer
#url = "http://arnetminer.org/person/qiaozhu-mei-633386.html"

    prefix = "http://arnetminer.org"
    url = prefix + URLSuffix
    urlName = URLSuffix[7:]

    #get URL of page
    html = urllib.urlopen(url).read()

    #write URL page
    newFile = open("arnetminer/"+urlName,'w')
    newFile.write(html)

def getAllChildren(URLSuffix):
#given a list of URLs get all URLS from arnetminer
    for link in URLSuffix:
        downloadPage(link)

def getINFO(name):
#get ID and affiliation from professor name off arnetminer
	url = "http://arnetminer.org/services/person/"
	url = url + name + "?u=oyster&o=tff"
	jsonString = urllib.urlopen(url).read()
	#print jsonString
	dict = json.loads(jsonString)[0]
	return dict["Id"], dict["Affiliation"]

def main():
    testFile = open("arnetminer/qiaozhuMei.html")
    html = testFile.read()
    soup = BeautifulSoup(html)

    #Retrieve all of the anchor tags
    tags = soup('a')

    for tag in tags:
        link = tag.get('href', None)
        URLSuffix = retrieveURLSuffix(link)

        #do not add any duplicates into the profiles list
        if URLSuffix not in profilesList and URLSuffix != None \
            and string.find(URLSuffix,"personbasic") < 0:
            profilesList.append(URLSuffix)

    getAllChildren(profilesList)

getID("eytan adar")