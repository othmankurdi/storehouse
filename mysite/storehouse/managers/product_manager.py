from datetime import datetime
from django.shortcuts import render
from mysite.storehouse.models import Product, User, Category


class ProductManager:

    def get_products(self):
        try:
            user_products = Product.objects.all().order_by('-create_date')
            return user_products
        except Exception as ex:
            print(f"Exception was occurred while retrieving user's product. Exception: {ex}")

    def get_user_products(self, auth_user_id):
        try:
            user_products = Product.objects.filter(user_id=User.objects.get(auth_user_id=auth_user_id)).order_by('-create_date')
            return user_products
        except Exception as ex:
            print(f"Exception was occurred while retrieving user's product. Exception: {ex}")

    def add_new_product(self, request):
        try:
            new_product = Product()
            new_product.name = request.POST.get('product_name')
            new_product.category = Category.objects.get(id=int(request.POST.get('category')))
            user = User.objects.get(auth_user_id=request.user.id)
            new_product.user = user
            new_product.save()
            return
        except Exception as ex:
            print(f'Exception was occurred while adding product. Exception: {ex}')

    def return_response_after_update(self, request, message):
        if request.POST.get('pagename') == 'myproducts':
            return render(request, 'storehouse/products.html',
                          {'products_list': self.get_user_products(request.user.id),
                           'message': message,
                           'user_name': request.user.username}, )
        else:
            return render(request, 'storehouse/home.html',
                          {'products_list': self.get_user_products(request.user.id),
                           'message': message,
                           'user_name': request.user.username}, )

    def update_product(self, request):
        try:
            user = User.objects.get(auth_user_id=request.user.id)
            if Product.objects.get(id=request.POST['product_id']).user_id == user.id:
                product_id = request.POST.get('product_id')
                product = Product.objects.get(id=product_id)
                product.name = request.POST.get('product_name')
                product.category = Category.objects.get(id=request.POST.get('category_id'))
                product.update_date = datetime.now()
                product.save()
                return self.return_response_after_update(request=request, message='Product has been successfully updated !')
            else:
                return self.return_response_after_update(request=request, message='User is not authorized to update this product, as user is not the owner !')
        except Exception as ex:
            print(f'Exception was occurred while updating product. Exception: {ex}')

    def delete_product(self, request):
        try:
            product = Product.objects.get(id=int(request.POST['product_id']))
            user = User.objects.get(auth_user_id=request.user.id)

            if product.user_id == user.id:
                product.delete()
                if request.POST.get('pagename') == 'myproducts':
                    products_list = self.get_products()
                    if products_list is None:
                        return render(request, 'storehouse/products.html',
                                      {'warningmessage': None,
                                       'messages': ["Product deleted successfully!", "You don't have Products!"],
                                       'user_name': request.user.username}, )
                    else:
                        return render(request, 'storehouse/products.html',
                                      {'products_list': products_list,
                                       'warningmessage': None,
                                       'messages': ["Product deleted successfully!", "Here is your Products:"],
                                       'user_name': request.user.username}, )
                else:
                    products_list = self.get_category_related_products(Category.objects.get(id=int(request.POST.get('category_id'))))
                    if products_list is None:
                        return render(request, 'storehouse/category_products.html',
                                      {'warningmessage': None,
                                       'messages': ["Product deleted successfully!", "You don't have Products!"],
                                       'user_name': request.user.username}, )
                    else:
                        return render(request, 'storehouse/category_products.html',
                                      {'products_list': products_list,
                                       'warningmessage': None,
                                       'messages': ["Product deleted successfully!", "Here is your Products:"],
                                       'user_name': request.user.username}, )
            else:
                products_list = self.get_products()
                if products_list is None:
                    return render(request, 'storehouse/home.html',
                                  {'warningmessage': "Product was not deleted!",
                                   'messages': ["User is not the owner to delete this prodduct",
                                                "You don't have Products!"],
                                   'user_name': request.user.username}, )
                else:
                    return render(request, 'storehouse/home.html',
                                  {'products_list': products_list,
                                   'warningmessage': "Product was not deleted!",
                                   'messages': ["Here is our Products!", ],
                                   'user_name': request.user.username}, )
        except Exception as ex:
            print(f'Exception was occurred while deleting product. Exception: {ex}')

    def get_category_related_products(self, category):
        try:
            products_list = Product.objects.filter(category=category)
            return products_list
        except Exception as ex:
            print(f"Exception was occurred while retrieving categoreis' related products. Exception: {ex}")

