from django.contrib import admin
from django.urls import path
from logapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('record/', views.record_usage, name='record_usage'),
    path('today/', views.today_logs, name='today_logs'),
    path('logs/', views.all_logs, name='all_logs'),
    path('perfumes/', views.perfume_management, name='perfume_management'),
    path('perfumes/add/', views.add_perfume, name='add_perfume'),
    path('perfumes/edit/<int:perfume_id>/', views.edit_perfume, name='edit_perfume'),
    path('perfumes/delete/<int:perfume_id>/', views.delete_perfume, name='delete_perfume'),
]
