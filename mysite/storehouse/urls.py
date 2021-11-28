from django.urls import path
from .apis.views import UserView, CategoryView, ProductView

app_name = 'storehouse'
urlpatterns = [
    path('', UserView.signup, name='index'),
    path('signup/', UserView.signup, name='signup'),
    path('login/', UserView.login, name='login'),
    path('logout/', UserView.logout, name='logout'),
    path('profile/', UserView.view_profile, name='profile'),
    path('edit_profile/', UserView.edit_profile, name='edit_profile'),
    path('products/', ProductView.get_user_products, name='products'),
    path('add_product/', ProductView.add_product, name='add_product'),
    path('edit_product/', ProductView.edit_product, name='edit_product'),
    path('delete_product/', ProductView.delete_product, name='delete_product'),
    path('add_category/', CategoryView.add_category, name='add_category'),
    path('category/', CategoryView.get_all_categories, name='category'),
    path('delete_category/', CategoryView.delete_category, name='delete_category'),
    path('rename_category/', CategoryView.rename_category, name='rename_category'),
    path('home/', ProductView.home, name='home'),
    path('category_related_products/', CategoryView.get_related_products, name='category_related_products'),

]
