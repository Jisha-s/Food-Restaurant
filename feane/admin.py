from django.contrib import admin

from feane.models import Book_table, Category, Posts, Product, Product_Category


# Register your models here.
 
admin.site.register(Posts)
admin.site.register(Category)
admin.site.register(Product_Category)
admin.site.register(Product)
admin.site.register(Book_table)