from django.shortcuts import render
from storehouse.managers import ProductManager
from storehouse.models import Product, Category
from django.views import View


class ProductView(View):

    def get_user_products(request):
        if request.method == 'GET':
            product_manager = ProductManager()
            products_list = product_manager.get_user_products(request.user.id)

            if products_list is None:
                return render(request, 'storehouse/products.html', {'warningmessage': "You don't have Products!",
                                                                  'user_name': request.user.username}, )
            else:
                return render(request, 'storehouse/products.html',
                              {'products_list': products_list, 'message': "Here is your Products:",
                               'user_name': request.user.username}, )

    def home(request):
        if request.method == 'GET':
            product_manager = ProductManager()
            products_list = product_manager.get_products()

            if products_list is None:
                return render(request, 'storehouse/home.html', {'warningmessage': "You don't have Products!",
                                                                  'user_name': request.user.username}, )
            else:
                return render(request, 'storehouse/home.html',
                              {'products_list': products_list, 'message': "Here is our Products:",
                               'user_name': request.user.username}, )

    def add_product(request):
        if request.method == 'GET':
            categories_list = Category.objects.all()
            return render(request, 'storehouse/add_product.html', {'categories_list': categories_list if request.POST.get('pagename') != 'category_products' else Category.objects.get(id=request.POST.get('category_id')), 'pagename': request.GET.get('pagename')})
        elif request.method == 'POST':
            product_manager = ProductManager()
            product_manager.add_new_product(request)
            if request.POST.get('pagename') == 'myproducts':
                products_list = product_manager.get_user_products(request.user.id)
                return render(request, 'storehouse/products.html',
                              {'products_list': products_list, 'message': "Here is your Products:",
                               'user_name': request.user.username}, )
            elif request.POST.get('pagename') == 'category_products':
                product_list = product_manager.get_category_related_products(Category.objects.get(id=int(request.POST.get('category'))))
                return render(request, 'storehouse/category_products.html',
                              {'products_list': product_list, 'message': "Here is your Products:",
                               'user_name': request.user.username}, )
            else:
                products_list = product_manager.get_products()
                return render(request, 'storehouse/home.html',
                              {'products_list': products_list, 'message': "Here is our Products:",
                               'user_name': request.user.username}, )

    def edit_product(request):
        if request.method == 'POST':
            product_manager = ProductManager()
            return product_manager.update_product(request)
        elif request.method == 'GET':
            if 'product_id' in request.GET:
                return render(request, 'storehouse/edit_product.html', {'product': Product.objects.get(id=request.GET.get('product_id')),
                                                                          'user_name': request.user.username,
                                                                          'categories_list': Category.objects.all(),
                                                                        'pagename': request.GET.get('pagename')}, )
            else:
                product_manager = ProductManager()

                return render(request, 'storehouse/products.html',
                              {'products_list': product_manager.get_products(),
                               'message': "please select a Product to edit",
                               'user_name': request.user.username}, )


    def delete_product(request):
        if request.method == 'POST':
            product_manager = ProductManager()
            is_deleted = product_manager.delete_product(request)
            return is_deleted