from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('menu/',views.menu,name='menu'),
    path('order/',views.order,name='order'),
    path('table/',views.table,name='table'),
    path('modifyTable/',views.modifyTable,name='modifyTable'),
    path('receipt/',views.receipt,name='receipt'),
    path('order/orderTable/',views.orderTable,name='orderTable'),
    path('recap/',views.recap,name='recap'),
    path('kitchen/',views.kitchen,name='kitchen'),

]