"""
urls.py - URL routing cho app shop
"""
from django.urls import path
from . import views

urlpatterns = [
    # Trang chủ
    path('', views.home, name='home'),

    # Sản phẩm
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),

    # Giỏ hàng
    path('cart/', views.cart, name='cart'),
    path('cart/add/', views.cart_add, name='cart_add'),
    path('cart/remove/<str:key>/', views.cart_remove, name='cart_remove'),
    path('cart/checkout/', views.checkout, name='checkout'),
    path('cart/order-success/<int:order_id>/', views.order_success, name='order_success'),

    # Tài khoản
    path('account/login/', views.login_view, name='login'),
    path('account/logout/', views.logout_view, name='logout'),
    path('account/register/', views.register_view, name='register'),

    # Admin panel (tên khác để không xung đột với /admin/ của Django)
    path('quan-tri/', views.admin_dashboard, name='admin_dashboard'),
    path('quan-tri/san-pham/', views.admin_products, name='admin_products'),
    path('quan-tri/san-pham/them/', views.admin_product_add, name='admin_product_add'),
    path('quan-tri/san-pham/sua/<int:pk>/', views.admin_product_edit, name='admin_product_edit'),
    path('quan-tri/san-pham/xoa/<int:pk>/', views.admin_product_delete, name='admin_product_delete'),
    path('quan-tri/don-hang/', views.admin_orders, name='admin_orders'),
    path('quan-tri/don-hang/<int:pk>/', views.admin_order_detail, name='admin_order_detail'),
    path('quan-tri/don-hang/<int:pk>/cap-nhat/', views.admin_order_update, name='admin_order_update'),
]
