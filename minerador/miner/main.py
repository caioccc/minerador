# -*- coding: UTF-8 -*-

"""Módulo principal.
"""
import requests
from bs4 import BeautifulSoup


def get_page_bs4(url):
    req = requests.get(url)
    if req.status_code == 200:
        page = BeautifulSoup(req.text, 'html.parser')
        return page
    return None


def get_title(page):
    return page.find_all('h1', id='product-name-default')[0].text


def get_desc(page):
    return page.find_all('div', 'info-description-frame-inside')[0].text


def get_price(page):
    return page.find_all('span', 'sales-price')[0].text


def get_installments(page):
    return page.find_all('p', 'payment-option')[0].text


def get_photo(page):
    return page.find_all('div', 'image-gallery-image')[0].img.attrs['src']


def miner_americanas():
    url = 'https://www.americanas.com.br/produto/76578099?pfm_carac=sofa&pfm_index=0&pfm_page=search&pfm_pos=grid&pfm_type=search_page%20&sellerId'
    page = get_page_bs4(url)
    if page:
        title = get_title(page)
        desc = get_desc(page)
        photo = get_photo(page)
        price = get_price(page)
        installments = get_installments(page)
        print(title, photo, price, installments)


def main():
    """Função principal da aplicação.
    """
    miner_americanas()


if __name__ == "__main__":
    main()
