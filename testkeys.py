import urllib
import os

f = open('keys.dat')
KEY = str(f.readline()).strip()
TOKEN = str(f.readline()).strip()
BOARD = str(f.readline()).strip()
f.close()

url = 'https://api.trello.com/1/boards/'+CARD+'/cards?key='+KEY+'&token='+TOKEN
print urllib.urlopen()

