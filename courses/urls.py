from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.course_search, name='course_search'),
    path('course_search', views.course_search_page, name='course_search_page'),
]