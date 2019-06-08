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
    message = '<b>' + tag + '</b>\n\n<pre>' + product.name + '</pre>\n\n<pre>Price: ' + product.price + '</pre>\n\n<pre>' + \
              product.installments + '</pre>\n<pre>Site: ' + product.site.name + '</pre>\n\n<pre>URL:</pre>' + \
              '<a href="' + product.url + '">link</a>'
    # message += (tag + str(': \n'))
    # message += (product.name + str(', \n'))
    # message += (product.price + str(', \n'))
    # message += (product.installments + str(', \n'))
    # message += ('Site: ' + product.site.name + str(', \n'))
    # message += ('Url: ' + product.url + str(', \n'))
    # message += ('Imagem: ' + product.photo_url)
    return message


class Miner(CommonMiner):
    def mine(self, url):
        page = self.get_page_bs4(url)
        if page:
            title = self.get_title(page)
            desc = self.get_desc(page)
            photo = self.get_photo(page)
            price = self.get_price(page)
            url = url
            sites = Site.objects.filter(name=self.get_store())
            if len(sites) > 0:
                site = sites[0]
            else:
                site = None
            installments = self.get_installments(page)
            logger.debug('Minerando: ' + title + "," + photo + "," + price + "," + site.name)
            print('Minerando: ', title, photo, price, installments)
            product = Product(name=title, desc=desc, price=price, installments=installments,
                              site=site, url=url, photo_url=photo)
            product.save()
            message = make_message('MINER', product)
            telegram_bot_sendtext(message)
            telegram_bot_sendphoto(product.photo_url)
        else:
            logger.error('Nao foi possivel abrir a page: ' + str(url))
            print('Nao foi possivel abrir a page: ', str(url))
            message = 'Nao foi possivel abrir a page: ', str(url)
            telegram_bot_sendtext(message)


class Reader(CommonMiner):
    def sync(self, product):
        url = product.url
        page = self.get_page_bs4(url)
        if page:
            title_new = self.get_title(page)
            desc_new = self.get_desc(page)
            photo_new = self.get_photo(page)
            price_new = self.get_price(page)
            url_new = url
            sites = Site.objects.filter(name=self.get_store())
            if len(sites) > 0:
                site_new = sites[0]
            else:
                site_new = None
            installments_new = self.get_installments(page)
            logger.debug('Reader: ' + title_new + "," + photo_new + "," + price_new + "," + site_new.name)
            print('Reader: ', title_new, photo_new, price_new, installments_new)
            message = make_message('READER', product)
            reader_bot_sendtext(message)
            # reader_bot_sendphoto(product.photo_url)

            products = Product.objects.filter(name=title_new, url=url_new)
            if len(products) > 0:
                product_db = products[0]
                price_prod_db = product_db.price.replace('R$ ', '').replace('.', '').replace(',', '.')
                price_new_rep = price_new.replace('R$ ', '').replace('.', '').replace(',', '.')
                if float(price_new_rep) > float(price_prod_db) or float(price_new_rep) < float(price_prod_db):
                    product_db.price = price_new
                    product_db.name = title_new
                    product_db.installments = installments_new
                    product_db.desc = desc_new
                    product_db.foto_url = photo_new
                    product_db.save()
                    logger.debug('CHANGED VALUE: ' + title_new + price_new + "," + site_new.name)
                    print('CHANGED VALUE: ', price_new, title_new, installments_new)
                    hist = History(product=product_db, price=price_new)
                    hist.save()

                    if float(price_new_rep) > float(price_prod_db):
                        pct = (float(price_new_rep) - float(price_prod_db)) / (float(price_prod_db))
                        label = str(int(pct * 100)) + "% Price UP"
                    else:
                        pct = (float(price_prod_db) - float(price_new_rep)) / (float(price_prod_db))
                        label = str(int(pct * 100)) + "% Price DOWN"
                    message = make_message('CHANGED VALUE ' + label, product_db)
                    telegram_bot_sendtext(message)
                    telegram_bot_sendphoto(product_db.photo_url)

            else:
                # product = Product(name=title_new, desc=desc_new, price=price_new, installments=installments_new,
                #                   site=site_new, url=url_new, foto_url=photo_new)
                # product.save()
                logger.debug(
                    'Produto nao existe, salvando: ' + title_new + "," + photo_new + "," + price_new + "," + site_new)
                print(title_new, photo_new, price_new, installments_new)

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
