from django.urls import path
from .views import store, cart, checkout, update_item, process_order, delete_session, product_view

urlpatterns = [
    path('', store, name='store'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('update_item/', update_item, name='update_item'),
    path('process_order/', process_order, name='process_order'),
    path('delete_session/', delete_session, name='delete_session'),
    path('product/<int:product_id>', product_view, name='product_view')
]
