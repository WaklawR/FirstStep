from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city',
                    'date_created', 'paid')
    list_filter = ('paid', 'date_created')
    list_display_links = ('first_name', 'email')
    search_fields = ('first_name', 'last_name', 'email', 'address')
    search_help_text = 'Enter order customer name or email address or address'
    inlines = (OrderItemInline,)
