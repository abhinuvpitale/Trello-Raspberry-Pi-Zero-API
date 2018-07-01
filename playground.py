import trelloParsers as tp

f = open('keys.dat')
KEY = str(f.readline()).strip()
TOKEN = str(f.readline()).strip()
BOARD = str(f.readline()).strip()
f.close()
url = 'https://api.trello.com/1/boards/'+BOARD+'/lists?cards=open&key='+KEY+'&token='+TOKEN
print tp.getCardsFromURL(url)