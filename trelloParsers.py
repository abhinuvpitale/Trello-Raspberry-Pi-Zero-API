import requests

def getCardsFromURL(url):
    '''
    Get All the cards from a url
    :param url: url request
    :return: dict of list of cards with key as the list name
    '''
    responseJSON = requests.get(url).json()
    response = {}
    for item in responseJSON:
        name = item['name']
        cards = []
        for inneritem in item['cards']:
            cards.append(inneritem['name'])
        response[name]=cards

    return response
