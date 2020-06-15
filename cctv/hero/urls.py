from django.urls import path
from . import views

urlpatterns = [
    path('main_vis', views.main_vis, name="main_vis"),
    path('menu_list', views.menu_list, name="menu_list"),
    
    path('gu_cctv', views.gu_cctv, name="gu_cctv"),
    path('gu_cctv2', views.gu_cctv2, name="gu_cctv2"),
    path('gu_crime', views.gu_crime, name="gu_crime"),
    path('gu_crime2', views.gu_crime2, name="gu_crime2"),
    
    path('gu_chart_1', views.gu_chart_1, name="gu_chart_1"),
    path('gu_chart_2', views.gu_chart_2, name="gu_chart_2"),
    path('gu_chart_3', views.gu_chart_3, name="gu_chart_3"),
    
    path('main_login', views.main_login, name="main_login"),
    path('main_logout', views.main_logout, name="main_logout"),
    path('main_login_wrong', views.main_login_wrong, name="main_login_wrong"),
    path('main_join', views.main_join, name="main_join"),
    path('main_join1', views.main_join1, name="main_join1"),
    
    path('gu_comp', views.gu_comp, name="gu_comp"),
]
