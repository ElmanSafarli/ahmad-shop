from django.shortcuts import get_object_or_404

from django.http import JsonResponse
from products.models import Category, Product

from django.views.generic import TemplateView, ListView, DetailView

def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = Category.objects.filter(parent_id=category_id).values('id', 'name', 'slug')

    # Add `has_subcategories` flag
    subcategories_list = list(subcategories)
    for subcategory in subcategories_list:
        subcategory['has_subcategories'] = Category.objects.filter(parent_id=subcategory['id']).exists()

    return JsonResponse({'subcategories': subcategories_list})

from django.views.generic import TemplateView
class HomeView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['newest_products'] = Product.objects.filter(in_stock=True).order_by('-id')[:16].only(
        'name', 'slug', 'price', 'discount_price', 'images', 'is_top_seller'
        )

        return context


class CategoryListView(ListView):
    model = Category
    template_name = 'category/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        """ Fetch only top-level categories (those without parents). """
        return Category.objects.filter(parent__isnull=True)

class CategoryDetailView(DetailView):
    template_name = 'category/category_detail.html'

    def get_object(self):
        """ Fetch category by slug. """
        category_slug = self.kwargs['category_slug']
        return get_object_or_404(Category, slug=category_slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        filters = self.request.GET

        # Get all descendant categories (subcategories)
        subcategories = category.children.all()
        subcategory_ids = subcategories.values_list('id', flat=True)

        # Retrieve products from the category and its subcategories
        products = Product.objects.filter(category__in=[category.id] + list(subcategory_ids))

        # Apply price filtering
        min_price = filters.get('min_price')
        max_price = filters.get('max_price')

        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)

        # Apply characteristics filtering
        characteristic_filters = {}
        for key, values in filters.lists():
            if key in ['min_price', 'max_price']:
                continue
            characteristic_filters[key] = values

        for name, values in characteristic_filters.items():
            products = products.filter(characteristics__name=name, characteristics__value__in=values)

        context['subcategories'] = category.children.all()
        context['products'] = products.distinct()
        context['category_path'] = category.get_category_path()
        
        # Get characteristics dynamically based on filtered products
        characteristics = {}
        for product in products:
            for characteristic in product.characteristics.all():
                if characteristic.name not in characteristics:
                    characteristics[characteristic.name] = set()
                characteristics[characteristic.name].add(characteristic.value)

        context['characteristics'] = {key: list(values) for key, values in characteristics.items()}
        return context


