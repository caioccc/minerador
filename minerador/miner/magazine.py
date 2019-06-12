# coding=utf-8
from minerador.miner.common import Reader, Miner


class CustomMiner(Miner):
    def get_title(self, page):
        try:
            title = page.find_all('h1', 'header-product__title')[0].text
            return title
        except:
            title = ''
            return title

    def get_desc(self, page):
        desc = page.find_all('div', 'description__container-text')
        if len(desc) == 0:
            desc = ''
        else:
            desc = page.find_all('div', 'description__container-text')[0].text
        return desc

    def get_price(self, page):
        price = page.find_all('span', 'price-template__text')
        try:
            if len(price) == 0:
                price = page.find_all('meta', {'itemprop': 'price'})[0].attrs['content']
            else:
                price = page.find_all('span', 'price-template__text')[0].text
        except:
            price = ''
        return price

    def get_installments(self, page):
        install = page.find_all('div', 'price-template')
        try:
            if len(install) == 0:
                install = ''
            else:
                install = page.find_all('div', 'price-template')[0].text
        except:
            install = ''
        return install

    def get_photo(self, page):
        try:
            fot = page.find_all('img', 'showcase-product__big-img')[0].attrs['src']
            return fot
        except:
            fot = ''
            return fot

    def get_store(self):
        return 'magazine'


class CustomReader(Reader):
    def get_title(self, page):
        try:
            title = page.find_all('h1', 'header-product__title')[0].text
            return title
        except:
            title = ''
            return title

    def get_desc(self, page):
        desc = page.find_all('div', 'description__container-text')
        if len(desc) == 0:
            desc = ''
        else:
            desc = page.find_all('div', 'description__container-text')[0].text
        return desc

    def get_price(self, page):
        price = page.find_all('span', 'price-template__text')
        try:
            if len(price) == 0:
                price = page.find_all('meta', {'itemprop': 'price'})[0].attrs['content']
            else:
                price = page.find_all('span', 'price-template__text')[0].text
        except:
            price = ''
        return price

    def get_installments(self, page):
        install = page.find_all('div', 'price-template')
        try:
            if len(install) == 0:
                install = ''
            else:
                install = page.find_all('div', 'price-template')[0].text
        except:
            install = ''
        return install

    def get_photo(self, page):
        try:
            fot = page.find_all('img', 'showcase-product__big-img')[0].attrs['src']
            return fot
        except:
            fot = ''
            return fot

    def get_store(self):
        return 'magazine'
