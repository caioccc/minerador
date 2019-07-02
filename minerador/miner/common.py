# coding=utf-8
import logging
import requests
from bs4 import BeautifulSoup

from minerador.bot.telegram_bot import telegram_bot_sendtext, telegram_bot_sendphoto, reader_bot_sendtext, \
    reader_bot_sendphoto
from minerador.models import Product, Site, History

sync_urls_delay = 60
check_new_minig_requests_delay = 10

logger = logging.getLogger(__name__)


def dict_gen(curs):
    ''' From Python Essential Reference by David Beazley
    '''
    import itertools
    field_names = [d[0].lower() for d in curs.description]
    while True:
        rows = curs.fetchmany()
        if not rows: return
        for row in rows:
            yield dict(itertools.izip(field_names, row))


def safe_unicode(obj, *args):
    """ return the unicode representation of obj """
    try:
        return unicode(obj, *args)
    except UnicodeDecodeError:
        # obj is byte string
        ascii_text = str(obj).encode('string_escape')
        return unicode(ascii_text)


def safe_str(obj):
    """ return the byte string representation of obj """
    try:
        return str(obj)
    except UnicodeEncodeError:
        # obj is unicode
        return unicode(obj).encode('unicode_escape')


class CommonMiner():
    def _get_categories(self, page):
        return []

    def get_url_no_bars_last(self, url):
        if url[len(url) - 1] == '/':
            url = url[:-1]
        return url

    def get_num_pages(self, page):
        return 1

    def get_url_paginated(self, url, paging):
        return ''

    def get_categories_link(self, page):
        urls = []
        categories = self._get_categories(page)
        for item in categories:
            if 'href' in item.attrs:
                urls.append(item.attrs['href'])
        return urls

    def get_products_urls(self, page):
        return []

    def get_page_bs4(self, url):
        req = requests.get(url)
        if req.status_code == 200:
            page = BeautifulSoup(req.text, 'html.parser')
            return page
        return None

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
        return ''

    def get_sku(self, page):
        return ''


def make_message(tag, product):
    if (product.name != '') and (product.installments != '') and (product.price != ''):
        message = '<b>' + tag + '</b>\n\n<pre>' + product.name + '</pre>\n\n<pre>Price: ' + product.price + '</pre>\n\n<pre>' + \
                  product.installments + '</pre>\n<pre>Site: ' + product.site.name + '</pre>\n\n<pre>URL:</pre>' + \
                  '<a href="' + product.url + '">link</a>'
    else:
        message = '<b>' + tag + '</b>\n\n<pre>' + product.name + '</pre>\n\n<pre>Price: ' + product.price + '</pre>\n\n<pre>' + \
                  '</pre>\n<pre>Site: ' + product.site.name + '</pre>\n\n<pre>URL:</pre>' + \
                  '<a href="' + product.url + '">link</a>'
    return message


def make_message_refresh(tag, product):
    if (product.name != '') and (product.price != ''):
        message = '<b>' + tag + '</b>\n\n<pre>' + product.name + '</pre>\n\n<pre>Price: ' + product.price + '</pre>' \
                  + '\n<pre>Site: ' + product.site.name + '</pre>\n\n<pre>URL:</pre>\n\n' + product.url
    else:
        message = '<b>' + tag + '</b>\n\n<pre>' + product.name + '</pre>\n\n<pre>Price: ' + product.price + '</pre>' \
                  + '\n<pre>Site: ' + product.site.name + '</pre>\n\n'
    return message


class Miner(CommonMiner):

    def mine(self, url):
        site_initial = self.get_page_bs4(url)
        if site_initial:
            print('Site: ', url)
            categories = self.get_categories_link(site_initial)
            for categorie_url in categories:
                categorie_url = self.get_url_no_bars_last(categorie_url)
                categorie_url_test = categorie_url + '?page=2'
                page_categorie = self.get_page_bs4(categorie_url_test)
                if page_categorie:
                    print('Categoria: ', categorie_url_test)
                    total_pages = self.get_num_pages(page_categorie)
                    print('total_pages: ', total_pages)
                    for paging in range(0, total_pages):
                        categorie_url_paging = self.get_url_paginated(categorie_url, (paging + 1))
                        page_categorie_bs = self.get_page_bs4(categorie_url_paging)
                        if page_categorie_bs:
                            print('Page: ', str(paging + 1))
                            products_page_categorie = self.get_products_urls(page_categorie_bs)
                            print(categorie_url_paging)
                            print(products_page_categorie)
                            for product_url in products_page_categorie:
                                page = self.get_page_bs4(product_url)
                                if page:
                                    title = self.get_title(page)
                                    desc = self.get_desc(page)
                                    photo = self.get_photo(page)
                                    price = self.get_price(page)
                                    url_prod = product_url
                                    sites = Site.objects.filter(name=self.get_store())
                                    if len(sites) > 0:
                                        site = sites[0]
                                    else:
                                        site = None
                                    installments = self.get_installments(page)
                                    print('Minerando: ', title)
                                    product = Product(name=title, desc=desc, price=price, installments=installments,
                                                      site=site, url=url_prod, photo_url=photo)
                                    product.save()
                                else:
                                    print('Nao foi possivel abrir a page prod: ', str(url_prod))
                                    break
                        else:
                            print('Nao foi possivel abrir a page categorie: ', str(categorie_url_paging))
                            break
            return True
        else:
            print('Nao foi possivel abrir a page site: ', str(url))
            return False


class Reader(CommonMiner):
    def sync(self, product):
        url = product.url
        try:
            page = self.get_page_bs4(url)
            if page:
                price_new = self.get_price(page)
                print('Reader: ', product.id, ' ', product.name)
                price_prod_db = product.price.replace('R$ ', '').replace('.', '').replace(',', '.')
                price_new_rep = price_new.replace('R$ ', '').replace('.', '').replace(',', '.')
                if product.history_set.count() == 0:
                    first_hist = History(product=product, price=product.price)
                    first_hist.save()
                try:
                    if float(price_new_rep) > float(price_prod_db) or float(price_new_rep) < float(price_prod_db):
                        product.price = price_new
                        product.save()
                        print('CHANGED VALUE: ', price_new, product.name)
                        hist = History(product=product, price=price_new)
                        hist.save()
                        if float(price_new_rep) > float(price_prod_db):
                            pct = (float(price_new_rep) - float(price_prod_db)) / (float(price_prod_db))
                            label = str(int(pct * 100)) + "% Price UP"
                        else:
                            pct = (float(price_prod_db) - float(price_new_rep)) / (float(price_prod_db))
                            label = str(int(pct * 100)) + "% Price DOWN"
                            if int(pct * 100) >= 5:
                                message = make_message('CHANGED VALUE ' + label, product)
                                bot_chatID_caio = '451429199'
                                bot_chatID_ll = '861252741'
                                res = reader_bot_sendtext(message, bot_chatID_caio)
                                res_2 = reader_bot_sendtext(message, bot_chatID_ll)
                                if 'error_code' in res:
                                    message = make_message_refresh('CHANGE VALUE', product)
                                    res = reader_bot_sendtext(message, bot_chatID_caio)
                                    print(res)
                                if 'error_code' in res_2:
                                    message = make_message_refresh('CHANGE VALUE', product)
                                    res_2 = reader_bot_sendtext(message, bot_chatID_ll)
                                    print(res_2)
                                reader_bot_sendphoto(product.photo_url, bot_chatID_caio)
                                reader_bot_sendphoto(product.photo_url, bot_chatID_ll)
                        print(label + ' ', price_new, product.name)
                except:
                    logger.debug(
                        'Erro ao tentar checar novo preco produto: ' + product.name)
        except:
            logger.info('PAGE NOT EXISTS: ' + product.url)

        """
        to = 'caiomarinho8@gmail.com'
        gmail_user = 'caiomarinho8@gmail.com'
        gmail_pwd = 'izszygyncvtfwicz'
        smtpserver = smtplib.SMTP("smtp.gmail.com",587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo
        smtpserver.login(gmail_user, gmail_pwd)
        header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:'+label+' - '+safe_str(title)+' \n'
        msg = header + '\n Price changed from '+str(dbprice)+' to '+str(price)+' \n\n'
        msg = msg + '\n\n '+url+' \n\n'
        smtpserver.sendmail(gmail_user, to, msg)
        smtpserver.close()"""

        # c.close()
        # db.close()
