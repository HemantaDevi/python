from builtins import str
from io import BytesIO
import io
import os
import re 
import time
from urllib import error
from urllib import request
from urllib.request import urlopen
from zipfile import ZipFile

from bs4 import BeautifulSoup
import requests

from entities.movie import Movie


# Subtitle Download Link
link = "https://subscene.com/subtitles/" 

#Get movie list from folder 
def getListOfMovies(pathToDirectory):
    movie_lists = []
    for root, dirs, files in os.walk(pathToDirectory, topdown=False):
        for name in dirs:
            movie_lists.append(Movie(name))
    return movie_lists

#Header
def getHeader():
    header = {'user-agent':'Mozilla/5.0 (Linux; Android 5.1; Lenovo P1ma40 Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.98 Mobile Safari/537.36'}
    return header

#Code to get access to movie page 
#With the release year and without the release year
def getMoviePage(movie, language):
    try:
        movieLink1 = link + str(movie.getMovieName()) + "-" + str(movie.getReleaseYear() + "/" + language)
        # print(movieLink1)
        time.sleep(5)
        req = request.Request(str(movieLink1), headers=getHeader())
        response = request.urlopen(req)
        time.sleep(5)
        response_page = response.read()
        # print("found with date")
        return response_page
    except error.HTTPError as e:
        if(e.code == 404):
            try:
                movieLink2 = link + str(movie.getMovieName() + "/" + language)
                # print(movieLink2)
                time.sleep(5)
                req = request.Request(str(movieLink2), headers=getHeader())
                response = request.urlopen(req)
                time.sleep(5)
                response_page = response.read()
                # print("found without date")
                return response_page
            except error.HTTPError as e:
                print(str(e.code) + movie.getMovieName())
        else:
            print(str(e.code) + movie.getMovieName())


#All English hyperlinks
def getHtmlPage(response_page,movie,language):
    
    soup = ""
    
    downloadLink="https://subscene.com"
    
    if response_page:
        soup= BeautifulSoup(response_page,"html.parser") 
    
        for linka in soup.find_all('a'):
            #print("line"+str(line)) 
            try:
                if((str(linka.contents[3].contents[0]).strip()==str(movie.getFolder()).strip())and(str(linka.contents[1].contents[0]).strip()==str(language).strip())):
                    return downloadLink+linka['href']
#                 if():
#                     print(linka)
            except IndexError as e:
                e
    else:
        print("no response page as error")

#Get download web page
def getWebpageFromFirstDownloadLink(downloadLink):
    time.sleep(5)
    req = request.Request(downloadLink, headers=getHeader())
    response = request.urlopen(req)
    time.sleep(3)
    response_page = response.read()
    return response_page

#Reach the html page containing the download option 
#reach the download option
def downloadSubtitleForMovie(secondWebPage):
    soup_link = BeautifulSoup(secondWebPage, "html5lib")
    
    downloadLink="https://subscene.com"
    
    for link in soup_link.find_all('a'):
        if 'download' in str(link):
            return downloadLink + link.get('href')

#Activate download link  
#download the zip file and extract the latter to the specific movie folder     
def activateDownloadLink(downloadLink, folderName, mainFolderPath):
    
    path = os.path.join(mainFolderPath, folderName);
    time.sleep(5)
    req = request.Request(downloadLink, headers=getHeader())
    response = request.urlopen(req)
    time.sleep(5)
    response_page = response.read()
    
    zipDocument = ZipFile(io.BytesIO(response_page))
    zipDocument.extractall(path)
    print("Downloaded and Extracted Successfully")
