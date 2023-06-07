from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.csoIndexPage, name='cso-index-page'),
    path('update/', views.csoUpdatePage, name='cso-update-page'),
    path('add/', views.csoAddPage, name='cso-add-page')


]
