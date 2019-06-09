from django.contrib import admin

# Register your models here.
from minerador.models import Product, Site, History


class SiteAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    list_display = ('url', 'id', 'name', 'done', 'created_at')


class ProductAdmin(admin.ModelAdmin):
    list_filter = ('site',)
    search_fields = (
        'name',
    )
    list_display = ('name', 'id', 'price', 'installments', 'site', 'count_history', 'updated_at')

    def count_history(self, obj):
        return obj.history_set.all().count()


class HistoryAdmin(admin.ModelAdmin):
    list_filter = ('product',)
    search_fields = (
        'product',
    )
    list_display = ('id', 'product', 'price', 'created_at')


admin.site.register(Site, SiteAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(History, HistoryAdmin)
