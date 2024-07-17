from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Order, OrderItem
from django.urls import reverse


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['post']


def order_detail(obj):
    url = reverse('orders:admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'phone',
                    'date', 'time', 'wish', 'paid',
                    'created', 'updated', order_detail]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
