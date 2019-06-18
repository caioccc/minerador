# coding=utf-8
import re

from common import Reader, Miner


class CustomMiner(Miner):
    def _get_categories(self, page):
        lists = page.find_all('a', 'link-of-menu')
        if len(lists) > 0:
            return lists[:28]
        return lists

    def get_url_paginated(self, url, paging):
        return str(str(self.get_url_no_bars_last(url)) + '?page=' + str(paging))

    def get_num_pages(self, page):
        list_links = page.find_all('a', {'role': 'button'})
        if len(list_links) > 0:
            if len(list_links) >= 2:
                word = list_links[len(list_links) - 2]
                if 'aria-label' in word.attrs:
                    if str(word.attrs['aria-label']).__contains__('Page'):
                        return int(word.text)
                    else:
                        return 1
                else:
                    return 1
            else:
                return 1
        return 1

    def get_products_urls(self, page):
        regex = re.compile('\s')
        l = [i.attrs['href'] for i in page.find_all('a', {'itemprop': 'url', 'data-product': regex})]
        if len(l) > 0:
            return l
        else:
            l = [i.attrs['href'] for i in page.find_all('a', {'name': 'linkToProduct'})]
            if len(l) > 0:
                return l
            else:
                print('nao encontrei produtos nesta page')
                return []

    def get_title(self, page):
        try:
            title = page.find_all('h1', id='product-name-default')[0].text
            return title
        except:
            title = ''
            return title

    def get_desc(self, page):
        desc = page.find_all('div', 'info-description-frame-inside')
        if len(desc) == 0:
            desc = ''
        else:
            desc = page.find_all('div', 'info-description-frame-inside')[0].text
        return desc

    def get_price(self, page):
        price = page.find_all('span', 'sales-price')
        try:
            if len(price) == 0:
                price = page.find_all('p', 'sales-price')[0].text
            else:
                price = page.find_all('span', 'sales-price')[0].text
        except:
            price = ''
        return price

    def get_installments(self, page):
        install = page.find_all('p', 'payment-option')
        if len(install) == 0:
            install = ''
        else:
            install = page.find_all('p', 'payment-option')[0].text
        return install

    def get_photo(self, page):
        try:
            fot = page.find_all('div', 'image-gallery-image')[0].img.attrs['src']
            return fot
        except:
            fot = ''
            return fot

    def get_store(self):
        return 'americanas'


class CustomReader(Reader):
    def get_title(self, page):
        try:
            title = page.find_all('h1', id='product-name-default')[0].text
            return title
        except:
            title = ''
            return title

    def get_desc(self, page):
        desc = page.find_all('div', 'info-description-frame-inside')
        if len(desc) == 0:
            desc = ''
        else:
            desc = page.find_all('div', 'info-description-frame-inside')[0].text
        return desc

    def get_price(self, page):
        price = page.find_all('span', 'sales-price')
        try:
            if len(price) == 0:
                price = page.find_all('p', 'sales-price')[0].text
            else:
                price = page.find_all('span', 'sales-price')[0].text
        except:
            price = ''
        return price

    def get_installments(self, page):
        install = page.find_all('p', 'payment-option')
        if len(install) == 0:
            install = ''
        else:
            install = page.find_all('p', 'payment-option')[0].text
        return install

    def get_photo(self, page):
        try:
            fot = page.find_all('div', 'image-gallery-image')[0].img.attrs['src']
            return fot
        except:
            fot = ''
            return fot

    def get_store(self):
        return 'americanas'
