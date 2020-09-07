from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *
from django.http import HttpResponse
import csv
import datetime

def print_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;'\
        'filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many\
    and not field.one_to_many]
    writer.writerow([field.verbose_name for field in fields])
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
print_csv.short_description = 'print'


admin.site.site_header = 'Warehouse Management System'
admin.site.site_title = 'Warehouse Management System'
admin.site.index_title = 'Warehouse Management System'

class CategoryAdmin(admin.ModelAdmin):
	list_display = ['category']
	actions = [print_csv]

class ItemAdmin(admin.ModelAdmin):
    list_display = ['items_ids', 'name', 'category', 'quantity']
    list_filter = ['name', 'category', 'quantity']
    actions = [print_csv]

class ClientAdmin(admin.ModelAdmin):
	list_display = ['place', 'description']
	actions = [print_csv]

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['trans_id', 'quantity', 'time', 'item', 'client']
    list_filter = ['quantity', 'time', 'item', 'client']
    actions = [print_csv]

admin.site.register(Client, ClientAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Transaction, TransactionAdmin)
