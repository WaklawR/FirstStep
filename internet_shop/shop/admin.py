from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Product, Category, Subcategory


class PriceRangeListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _("Диапазон цен")

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "range"

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return [
            ("1-100", _("1-100")),
            ("100-1000", _("100-1000")),
            ("1000-...", _("1000-...")),
        ]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == "1-100":
            return queryset.filter(
                price__lte=100.0,
            )
        if self.value() == "100-1000":
            return queryset.filter(
                price__gt=100.0,
                price__lte=1000.0,
            )
        if self.value() == "1000-...":
            return queryset.filter(
                price__gt=1000.0,
            )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock',
                    'available', 'subcategory')
    list_filter = (PriceRangeListFilter, 'stock', 'available')
    search_fields = ('name', 'subcategory__name')
    actions = ("nullify_stock",)

    @admin.action(description="Обнулить наличие товара на складе")
    def nullify_stock(cls, request, queryset):
        queryset.update(stock=0, available=False)

    # @admin.display(ordering='subcategory__name', description='Subcategory')
    # def get_subcategory(self, obj):
    #     return obj.subcategory.name


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name', 'category__name')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

