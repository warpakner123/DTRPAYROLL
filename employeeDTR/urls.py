from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name="base"),
    path('login-page',views.login_page, name='login-page'),
    path('upload-xls', views.upload_xls, name="upload-xls"),
    path('employee-dashboard', views.empdb, name='empplyee-dashboard'),
    path('home', views.home,name='home'),
]
