import requests
import pprint
import csv
from bs4 import BeautifulSoup

class CostApartment():
    def __init__(self):
        self._domain = 'https://chelyabinsk.n1.ru'
        self._URL = f'{self._domain}/kupit/kvartiry/vtorichka/district-Kalininskiy-rayon/'

        self._response = requests.get(self._URL)
        self._soup = BeautifulSoup(self._response.text, 'html.parser')

        self._lst_result = []

    def _ini_dic(self):
        dic = {}
        dic['region'] = ''
        dic['city'] = ''
        dic['address'] = ''
        dic['characteristic'] = ''
        dic['price'] = ''
        return dic


    def data_search(self):
        div_tags = self._soup.find_all('div', class_='living-list-card__main-container')

        self._lst_result = []
        for v1 in div_tags:
            dic = self._ini_dic()

            tags = v1.find('a', class_='link')
            #print(tags.text)
            dic['address'] = tags.text

            tags = v1.find('div', class_='search-item-district')
            #print(  tags.text )
            dic['region'] = tags.text

            tags = v1.find('div', class_='living-list-card__city-with-estate')
            #print(tags.text)
            dic['city'] = tags.text

            tags = v1.find('div', class_='living-list-card__area')
            #print(tags.text)
            dic['characteristic'] += tags.text

            tags = v1.find('div', class_='living-list-card__floor')
            #print(tags.text)
            dic['characteristic'] += " " + tags.text

            tags = v1.find('div', class_='living-list-card__material')
            #print(tags.text)
            dic['characteristic'] += " " + tags.text

            tags = v1.find('div', class_='living-list-card-price__item _object')
            #print(tags.text)
            dic['price'] = (tags.text).replace(chr(160), ' ') + 'руб'

            self._lst_result.append(dic)
            #print('...')

        print('-------------------------------------------------------------------------------')
        pprint.pprint( self._lst_result )
        return self._lst_result

    def cost_min(self):
        lst = self.data_search()
        vMin = [999999999999.0,-1]

        for i,v in enumerate(lst):
            s = v['price'].replace(' ','')
            sn = s[:-3]
            t = float( sn )
            if t < vMin[0]:
                vMin[0] = t
                vMin[1] = i
        if vMin[1] == -1:
            return []
        else:
            d = lst[vMin[1]]
            s = 'минимальная цена: ' + d['price'] + '\n'
            s += 'город: ' + d['city'] + '\n'
            s += d['address'] + '\n'
            s += d['region'] + '\n'
            s += 'характеристика: ' + d['characteristic']
            return s

    def cost_max(self):
        lst = self.data_search()
        vMax = [0.0,-1]

        for i,v in enumerate(lst):
            s = v['price'].replace(' ','')
            sn = s[:-3]
            t = float( sn )
            if t > vMax[0]:
                vMax[0] = t
                vMax[1] = i
        if vMax[1] == -1:
            return []
        else:
            d = lst[ vMax[1] ]
            s = 'максимальная цена: '+ d['price']+'\n'
            s += 'город: ' + d['city']+ '\n'
            s += d['address']+'\n'
            s += d['region'] + '\n'
            s += 'характеристика: '+d['characteristic']
            return s


if __name__ == '__main__':
    ca = CostApartment()
    sMin = ca.cost_min()
    sMax = ca.cost_max()
    print('\n*********************************************************************')
    print(  sMin  )
    print(sMax)






