# coding:UTF-8
from datetime import datetime
from multiprocessing import Process, Queue
from threading import Thread

from django.db.models import Q, Count
from django.utils.html import escape
from django.views.generic import TemplateView, ListView, DetailView
from django_datatables_view.base_datatable_view import BaseDatatableView

from minerador.miner.explorer import mineData, syncTracks
from minerador.models import Product
from minerador.templatetags.customtags import mediadez, mediacinco


class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        Thread(target=mineData).start()
        Thread(target=syncTracks).start()
        # lista = Product.objects.order_by('?')
        # total = (lista.count() / 1000)
        # print('total: ', total)
        # for i in range(0, total):
        #     if i == 11:
        #         Thread(target=syncTracks, args=(lista[i * 1000:], i)).start()
        #     else:
        #         Thread(target=syncTracks, args=(lista[i * 1000:((i * 1000) + 999)], i)).start()
        return super(IndexView, self).get(request, *args, **kwargs)


# class ProductDetailView(DetailView):
#     model = Product
#     pk_url_kwarg = 'pk'
#     context_object_name = 'produto'
#     template_name = 'detail.html'
#
#     def get(self, request, *args, **kwargs):
#         top_prods = Product.objects.annotate(num_history=Count('history')) \
#                         .order_by('-num_history')[:2]
#         print(top_prods)
#         return super(ProductDetailView, self).get(request, *args, **kwargs)
#
#
# class ListBestView(TemplateView):
#     template_name = 'list_best.html'
#
#
# class OrderListJson(BaseDatatableView):
#     model = Product
#     columns = ['photo_url', 'id', 'name', 'price', 'history', 'url', 'created_at', 'updated_at']
#     order_columns = ['id', 'price', 'updated_at', 'created_at', 'name', 'url']
#     max_display_length = 500
#
#     def render_column(self, row, column):
#         if column == 'history':
#             total = row.history_set.count()
#             return escape('{0}'.format(total))
#         elif column == 'created_at':
#             type(row.created_at)
#             date = row.created_at.strftime("%d-%m-%Y %H:%M:%S")
#             return date
#         elif column == 'updated_at':
#             type(row.created_at)
#             date = row.updated_at.strftime("%d-%m-%Y %H:%M:%S")
#             return date
#         else:
#             return super(OrderListJson, self).render_column(row, column)
#
#     def filter_queryset(self, qs):
#         search = self.request.GET.get('search[value]', None)
#         if search:
#             qs = qs.filter(Q(name__icontains=search) | Q(price__istartswith=search) | Q(id__istartswith=search) |
#                            Q(created_at__istartswith=search) | Q(updated_at__istartswith=search))
#         return qs
#
#
# class ListBestJson(OrderListJson):
#     def get_initial_queryset(self):
#         if not self.model:
#             raise NotImplementedError("Need to provide a model or implement get_initial_queryset!")
#         dict = self.model.objects.all()
#         ids = [product.id for product in Product.objects.all() if mediadez(product) or mediacinco(product)]
#         return Product.objects.filter(id__in=ids)
