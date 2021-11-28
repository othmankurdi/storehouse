from django.contrib import admin
from storehouse.models import User, Product, Category
from storehouse.admin.admin_models import UserAdmin, ProductAdmin, CategoryAdmin

admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
