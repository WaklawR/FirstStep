from django.core.cache import cache
from django.views.generic import ListView, DetailView, TemplateView

from .models import Product


class ProductList(ListView):
    model = Product
    template_name = "products.html"
    context_object_name = 'products'
    paginate_by = 100
    ordering = ["subcategory"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active"] = "Products"
        return context


class ProductDetails(DetailView):
    model = Product
    template_name = "product.html"
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active"] = "Product"
        return context

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'product-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'product-{self.kwargs["pk"]}', obj)

        return obj


class HomeView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active"] = "Home"
        return context
