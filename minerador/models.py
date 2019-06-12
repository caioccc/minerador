from __future__ import unicode_literals

from django.db import models


# Create your models here.


class TimeStamped(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Site(TimeStamped):
    url = models.CharField(max_length=300, blank=True, null=True)
    done = models.BooleanField(default=False)
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return "%s" % self.name

    def __unicode__(self):
        return "%s" % self.name


class Product(TimeStamped):
    name = models.CharField(max_length=300, blank=True, null=True)
    desc = models.TextField(blank=True, null=True)
    price = models.CharField(max_length=100, blank=True, null=True)
    installments = models.TextField(blank=True, null=True)
    sku = models.CharField(max_length=100, blank=True, null=True)
    site = models.ForeignKey(Site, blank=True, null=True)
    url = models.CharField(max_length=300, blank=True, null=True)
    photo_url = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return "%s" % self.name

    def __unicode__(self):
        return "%s" % self.name


class History(TimeStamped):
    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.CASCADE)
    price = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return "%s" % self.product

    def __unicode__(self):
        return "%s" % self.product


class HistoricSummary(History):
    class Meta:
        proxy = True
        verbose_name = 'Historic Summary'
        verbose_name_plural = 'Historic Summaries'
