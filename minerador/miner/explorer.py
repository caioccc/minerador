# coding=utf-8
import time

import americanas
from common import sync_urls_delay, check_new_minig_requests_delay
from minerador.miner import magazine
from minerador.models import Product, Site

readers = {"americanas": americanas.CustomReader,
           # "magazine": magazine.CustomReader
           }

miners = {"americanas": americanas.CustomMiner,
          # "magazine": magazine.CustomMiner
          }


def syncTracks():
    while True:
        products = Product.objects.all()
        for product in products:
            customreader = readers[product.site.name]()
            customreader.sync(product)
            time.sleep(5)
        time.sleep(60)


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
