from django.contrib import admin
from .models import ProductType, Product, ProductCharacteristic, Category
from modeltranslation.admin import TranslationAdmin

@admin.register(ProductType)
class ProductTypeAdmin(TranslationAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


class ProductCharacteristicInline(admin.TabularInline):
    model = ProductCharacteristic
    extra = 1


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = ('name', 'brand', 'price', 'discount_price', 'product_type', 'category', 'discount_percentage')  # Added 'category' here
    list_filter = ('brand', 'product_type', 'category')  # Added 'category' to filter
    search_fields = ('name', 'brand', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductCharacteristicInline] 

    def discount_percentage(self, obj):
        return f"{obj.discount_percentage():.2f}%"
    discount_percentage.short_description = "Discount %"


@admin.register(ProductCharacteristic)
class ProductCharacteristicAdmin(TranslationAdmin):
    list_display = ('product', 'name', 'value')
    search_fields = ('name', 'value')
    list_filter = ('product',)


@admin.register(Category) 
class CategoryAdmin(TranslationAdmin):
    list_display = ('name', 'parent', 'slug')  
    search_fields = ('name',) 
    prepopulated_fields = {'slug': ('name',)}  
    list_filter = ('parent',)  


