# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from apps.home.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [

    # The home page
    path('', DashBoard.as_view(), name='home'),
    path( 'view_product/', ProductView.as_view(), name='product_view' ),

    # Matches any html file
    re_path('userlist/', views.UserListView, name='userlist'),
    re_path( 'register_product/', register_product.as_view(), name='register_product' ),
    re_path( 'add_category/', ProductCategoryAdd.as_view(), name='add_category' ),
    # re_path(r'^.*\.*', views.pages, name='pages'), 
    path('delete/<int:id>', views.delete, name='delete'),
    path('update/<int:product_id>/', UpdateProductView.as_view(), name='update_product'),
    path('bonushistory/',bonus.as_view(),name='bonushistory'),
    path('profile/',userprofile.as_view(),name='profile')
    # path('update/<int:id>', views.update, name='update'),
    # path('update/updaterecord/<int:id>', views.updaterecord, name='updaterecord'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()