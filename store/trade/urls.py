from django.urls import path
from .import views


urlpatterns =[
    path('',views.home,name='home'),
    
    path('category/<int:id>/', views.category_products, name='category_products'),
    path('product/<int:id>/', views.product_detail, name='detail'),
    path('search/', views.search, name='search'),

    #panier#

    path('cart/', views.cart_detail, name='cart_detail'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/<int:id>/', views.update_cart, name='update_cart'),

    #commande#
    path('checkout/', views.checkout, name='checkout'),
    path('paiement/', views.paiement, name='paiement'),


    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('adm/products/', views.product_dashboard, name='product_dashboard'),
    path('adm/products/add/', views.add_product, name='add_product'),
    path('adm/products/edit/<int:id>/', views.edit_product, name='edit_product'),
    path('adm/products/delete/<int:id>/', views.delete_product, name='delete_product'),
    path('dashboard/users/', views.users_list, name='users_list'),
   
    path('dashboarde/', views.main_dashboard, name='main_dashboard'),
    path('dashboard/categories/', views.category_dashboard, name='category_dashboard'),

    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('upload-profile-image/', views.upload_profile_image, name='upload_profile_image'),

]
