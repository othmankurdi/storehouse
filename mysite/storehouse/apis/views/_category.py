from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from storehouse.managers import CategoryManager, ProductManager
from storehouse.models import Category


class CategoryView:

    def get_all_categories(request):
        if request.method == 'GET':
            category_manager = CategoryManager()
            categories_list = category_manager.get_categories()
            if categories_list is None:
                return render(request, 'storehouse/category.html', {'warningmessage': "You don't have Categories!",
                                                                    'user_name': request.user.username}, )
            else:
                return render(request, 'storehouse/category.html',
                              {'categories_list': categories_list, 'message': "Here is your Categories:",
                               'user_name': request.user.username}, )

    def add_category(request):
        if request.method == 'GET':
            return render(request, 'storehouse/add_category.html')
        elif request.method == 'POST':
            new_category = Category()
            new_category.name = request.POST['category_name']
            new_category.save()
            category_manager = CategoryManager()
            return render(request, 'storehouse/category.html',
                              {'categories_list': category_manager.get_categories(),
                               'message': "Category is added successfully!",
                               'user_name': request.user.username}, )

    def delete_category(request):
        if request.method == 'POST':
            category_manager = CategoryManager()
            category_manager.delete_category(request.POST['category_id'])
            categories_list = category_manager.get_categories()
            if categories_list is None:
                return render(request, 'storehouse/category.html', {'warningmessage': "You don't have Categories!",
                                                                    'user_name': request.user.username}, )
            else:
                return render(request, 'storehouse/category.html',
                              {'categories_list': categories_list, 'message': "Here is the Categories:",
                               'user_name': request.user.username}, )

    def rename_category(request):
        if request.method == 'POST':
            category_manager = CategoryManager()
            if request.user.is_staff:
                category = Category.objects.get(id=int(request.POST.get('category_id')))
                category.name = request.POST.get('category_name')
                category.save()
                return render(request, 'storehouse/category.html',
                              {'categories_list': category_manager.get_categories(),
                               'message': "Category has been successfully renamed !",
                               'user_name': request.user.username}, )
            else:
                return render(request, 'storehouse/category.html',
                              {'categories_list': category_manager.get_categories(),
                               'message': "User is not Authorized to update a Category !",
                               'user_name': request.user.username}, )
                #this cae can be replaced with another template with no posibility to rename a category

        elif request.method == 'GET':
            return render(request, 'storehouse/rename_category.html',
                          {'category': Category.objects.get(id=int(request.GET.get('category_id'))),
                           'user_name': request.user.username}, )

    def get_related_products(request):
        if request.method == 'GET':
            product_manager = ProductManager()
            category = Category.objects.get(id=request.GET['category_id'])
            products_list = product_manager.get_category_related_products(category=category)
            if products_list is None:
                return render(request, 'storehouse/category_products.html', {'warningmessage': "This Category has no related Products",
                                                                             'user_name': request.user.username,
                                                                             'category_id': request.GET['category_id']}, )
            else:
                return render(request, 'storehouse/category_products.html',
                              {'products_list': products_list, 'message': "Here is the Category related Products:",
                               'user_name': request.user.username,
                               'category_id': request.GET['category_id']}, )
