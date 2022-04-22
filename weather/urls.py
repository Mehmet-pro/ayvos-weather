from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('weather/<city>/',views.weather,name="weather"),
    path('log/<int:user_id>',views.log_view,name="logs"),
    path('login/',views.login_view,name="login"),
    path('logout/',views.logout_view,name="logout")
]