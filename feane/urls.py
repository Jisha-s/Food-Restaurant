from feane import views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.index, name='index'),
    path('menu/', views.menu, name='menu'),
    path('about/', views.about, name='about'),
    path('book_table/bookingForm', views.book_table, name='book_table'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
    path('edit_cart_item/', views.edit_cart_item, name='edit_cart_item'),
    path('register/', views.register, name='register'),
    path('checkout/', views.checkout, name='checkout'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    # path('imageprediction/', views.my_aipage, name='my_aipage'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 