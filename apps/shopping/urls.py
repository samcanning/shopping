from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^product/(?P<product>\d+)$', views.productpage),
    url(r'^category/(?P<category>\d+)$', views.categorypage),
    url(r'^category/(?P<category>\d+)/(?P<subcategory>\d+)$', views.subcategorypage),
    url(r'^newproducts$', views.newproducts),
    url(r'^newcategory$', views.newcategory),
    url(r'^newsubcategory$', views.newsubcategory),
    url(r'create$', views.create),
    url(r'cart$', views.cart),
    url(r'addtocart/(?P<product>\d+)$', views.addtocart),
    url(r'removefromcart/(?P<product>\d+)$', views.removefromcart),
]