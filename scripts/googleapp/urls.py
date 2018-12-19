from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('apps/', views.AppListView.as_view(), name='apps'),
    path('apps/<int:pk>/', views.AppDetailView.as_view(), name='app_detail'),
    path('apps/new/', views.AppCreateView.as_view(), name='app_new'),
    path('apps/<int:pk>/delete/', views.AppDeleteView.as_view(), name='app_delete'),
    path('apps/<int:pk>/update/', views.AppUpdateView.as_view(), name='app_update'),
    path('sites/filter/', views.AppFilterView.as_view(), kwargs=None, name='filter'),
]