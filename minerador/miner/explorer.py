# coding=utf-8
import time

import americanas
from common import sync_urls_delay, check_new_minig_requests_delay
from minerador.miner import magazine
from minerador.models import Product, Site
from datetime import datetime

readers = {
    # "americanas": americanas.CustomReader,
    "magazine": magazine.CustomReader
}

miners = {
    # "americanas": americanas.CustomMiner,
    "magazine": magazine.CustomMiner
}
# def syncTracks():
#     while True:
#         print('Start ID: ', datetime.now())
#         products = Product.objects.order_by('?')
#         for product in products:
#             customreader = readers[product.site.name]()
#             customreader.sync(product)
#             time.sleep(2)
#         time.sleep(1)


def syncTracks(products, i):
    while True:
        print('Start ID: ', i)
        # products = Product.objects.order_by('?')
        for product in products:
            customreader = readers[product.site.name]()
            customreader.sync(product)
            time.sleep(3)
        time.sleep(1)


def mineData():
    while True:
        sites = Site.objects.filter(done=False)
        for site in sites:
            domain = site.name
            miner = miners[domain]()
            result = miner.mine(site.url)
            if result:
                site.done = True
                site.save()
        time.sleep(check_new_minig_requests_delay)


# def count_reader(products):
#     startTime = datetime.now()
#     print('Start code: ', datetime.now())
#     # products = Product.objects.order_by('?')
#     i = 0
#     for product in products:
#         i = i + 1
#         if i == 10:
#             print('product 10: ', datetime.now())
#         if i == 100:
#             print('product 100: ', datetime.now())
#         if i == 1000:
#             print('product 1000: ', datetime.now())
#         if i == 5000:
#             print('product 5000: ', datetime.now())
#         if i == 10000:
#             print('product 10000: ', datetime.now())
#         customreader = readers[product.site.name]()
#         customreader.sync(product)
#         time.sleep(3)
#     print('Finish code: ', datetime.now())
