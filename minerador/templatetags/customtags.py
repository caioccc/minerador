import calendar
import time
from datetime import datetime
from decimal import Decimal

from django import template

register = template.Library()


def utc_mktime(utc_tuple):
    """Returns number of seconds elapsed since epoch

    Note that no timezone are taken into consideration.

    utc tuple must be: (year, month, day, hour, minute, second)

    """

    if len(utc_tuple) == 6:
        utc_tuple += (0, 0, 0)
    return time.mktime(utc_tuple) - time.mktime((1970, 1, 1, 0, 0, 0, 0, 0, 0))


@register.filter
def to_timestamp(value):
    """Removes all values of arg from the given string"""
    return int(utc_mktime(value.timetuple())) * 1000


@register.filter
def replace_dot(value):
    if len(value) <= 6:
        return value.replace(',', '.')
    else:
        value = value.replace('.', '', 1)
        return value.replace(',', '.')


@register.filter
def isdown(produto):
    if produto.history_set.count() > 1:
        lista = produto.history_set.all()
        last_price = replace_dot(lista[lista.count() - 2].price)
        current_price = replace_dot(lista[lista.count() - 1].price)
        if float(last_price) > float(current_price):
            return True
    return False


@register.filter
def count_percentage(produto):
    if produto.history_set.count() > 1:
        lista = produto.history_set.all()
        last_price = float(replace_dot(lista[len(lista) - 2].price))
        current_price = float(replace_dot(lista[len(lista) - 1].price))
        if current_price > last_price:
            pct = (current_price - last_price) / (last_price)
            label = str(int(pct * 100)) + "%"
        else:
            pct = (last_price - current_price) / (last_price)
            label = str(int(pct * 100)) + "%"
        return label
    return '-'


def median_value(queryset, term):
    count = int(queryset.count())
    values = queryset.values_list(term, flat=True).order_by(term)
    convert_values = map(replace_dot, values)
    values = map(float, [val for val in convert_values if val != ''])
    if count == 0:
        return sum(values)
    return sum(values) / count


@register.filter
def mediadez(produto):
    try:
        priceProduct = float(replace_dot(produto.price))
    except(Exception,):
        priceProduct = '0.00'
    median = median_value(produto.history_set, 'price')
    return priceProduct <= (median - (median * 0.1))


@register.filter
def mediacinco(produto):
    try:
        priceProduct = float(replace_dot(produto.price))
    except(Exception,):
        priceProduct = '0.00'
    median = median_value(produto.history_set, 'price')
    return priceProduct <= (median - (median * 0.05))


@register.filter
def mediadois(produto):
    try:
        priceProduct = float(replace_dot(produto.price))
    except(Exception,):
        priceProduct = '0.00'
    median = median_value(produto.history_set, 'price')
    return priceProduct <= (median - (median * 0.02))
