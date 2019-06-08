# coding=utf-8
from common import Reader, Miner


class CustomMiner(Miner):
    def get_title(self, page):
        return page.find_all('h1', id='product-name-default')[0].text

    def get_desc(self, page):
        desc = page.find_all('div', 'info-description-frame-inside')
        if len(desc) == 0:
            desc = ''
        else:
            desc = page.find_all('div', 'info-description-frame-inside')[0].text
        return desc

    def get_price(self, page):
        price = page.find_all('span', 'sales-price')
        if len(price) == 0:
            price = page.find_all('p', 'sales-price')[0].text
        else:
            price = page.find_all('span', 'sales-price')[0].text
        return price

    def get_installments(self, page):
        install = page.find_all('p', 'payment-option')
        if len(install) == 0:
            install = ''
        else:
            install = page.find_all('p', 'payment-option')[0].text
        return install

    def get_photo(self, page):
        return page.find_all('div', 'image-gallery-image')[0].img.attrs['src']

    def get_store(self):
        return 'americanas'


class CustomReader(Reader):
    def get_title(self, page):
        return page.find_all('h1', id='product-name-default')[0].text

    def get_desc(self, page):
        desc = page.find_all('div', 'info-description-frame-inside')
        if len(desc) == 0:
            desc = ''
        else:
            desc = page.find_all('div', 'info-description-frame-inside')[0].text
        return desc

    def get_price(self, page):
        price = page.find_all('span', 'sales-price')
        if len(price) == 0:
            price = page.find_all('p', 'sales-price')[0].text
        else:
            price = page.find_all('span', 'sales-price')[0].text
        return price

    def get_installments(self, page):
        install = page.find_all('p', 'payment-option')
        if len(install) == 0:
            install = ''
        else:
            install = page.find_all('p', 'payment-option')[0].text
        return install

    def get_photo(self, page):
        return page.find_all('div', 'image-gallery-image')[0].img.attrs['src']

    def get_store(self):
        return 'americanas'
