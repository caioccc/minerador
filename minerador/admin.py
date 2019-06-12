from django.contrib import admin

# Register your models here.
from django.db.models import Count, Sum, Avg, Min, Max

from minerador.models import Product, Site, History, HistoricSummary


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


@admin.register(HistoricSummary)
class SaleSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/hist_summary_change_list.html'
    date_hierarchy = 'created_at'

    # def get_changelist(self, request, **kwargs):
    #     return super(SaleSummaryAdmin, self).get_changelist(request, **kwargs)

    def changelist_view(self, request, extra_context=None):
        response = super(SaleSummaryAdmin, self).changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
            'total': Count('id'),
            'avg': Avg('price'),
            'min': Min('price'),
            'max': Max('price')
        }
        response.context_data['summary'] = list(qs.values('product__name').annotate(**metrics).order_by('-price'))
        return response


admin.site.register(Site, SiteAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(History, HistoryAdmin)
