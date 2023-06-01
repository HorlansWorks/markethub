from django.urls import path

from .views import *

urlpatterns = [
    path('', home_page),
    path('products/', Products.as_view()),
    path('users/create', CreateUser.as_view()),
    # path('users/login', Login.as_view()),
    path('users/logout', LogOut.as_view()),
    path('users/all', ListUsers.as_view()),
    path('users/profile', UserAccount.as_view()),
    path('users/<uuid:uid>', UserById.as_view()),
    path('products/<uuid:product_id>/', ProductById.as_view()),
    path('products/users/<uuid:user_id>/', get_product_by_user_id),
    # path('products/category/<int:product_category>/',
    #      products_by_category),
]
