from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Product

class ProductsListView(ListView):
    model = Product
    template_name = 'products/products_list.html'

    def get_queryset(self):
        queryset = Product.objects.all()
        filters = self.request.GET

        min_price = filters.get('min_price')
        max_price = filters.get('max_price')

        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        characteristic_filters = {}

        for key, values in filters.lists():
            if key in ['min_price', 'max_price', 'sort']: 
                continue
            characteristic_filters[key] = values 

        for name, values in characteristic_filters.items():
            queryset = queryset.filter(characteristics__name=name, characteristics__value__in=values)

        sort_order = filters.get('sort')
        if sort_order == 'cheap_first':
            queryset = queryset.order_by('price')  
        elif sort_order == 'expensive_first':
            queryset = queryset.order_by('-price') 
        else:
            queryset = queryset.order_by('-published_date')

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        characteristics = {}
        for product in context['object_list']:
            for characteristic in product.characteristics.all():
                if characteristic.name not in characteristics:
                    characteristics[characteristic.name] = set()
                characteristics[characteristic.name].add(characteristic.value)

        context['characteristics'] = {key: list(values) for key, values in characteristics.items()}
        
        return context

class ProductDetailView(DetailView):
    model = Product 
    template_name = 'products/product_detail.html'
    context_object_name = 'product' 

    def get_object(self):
        """ Fetch product by slug. """
        return get_object_or_404(Product, slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        
        # Example: Fetch related products from the same category
        context['related_products'] = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

        return context