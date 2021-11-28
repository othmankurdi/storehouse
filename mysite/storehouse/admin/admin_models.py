from django.contrib import admin
from django.db import models


class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'password', 'age', 'bio')
    search_fields = ('email', 'full_name')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_name', 'user_full_name', 'create_date', 'update_date')
    search_fields = ('name', 'category__name', 'user__full_name')

    def category_name(self, obj):
        return obj.category.name

    def user_full_name(self, obj):
        return obj.user.full_name
