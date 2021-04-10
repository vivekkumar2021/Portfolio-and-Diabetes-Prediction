from django.urls import path
from . import views

urlpatterns = [
        path('',views.index,name='index'),
        path('about',views.about,name='about'),
        path('login',views.login,name='login'),
        path('register',views.register,name='register'),
        path('predict/',views.predict,name='predict'),
        path('predict/result',views.result),
        ]