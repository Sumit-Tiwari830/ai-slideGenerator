from django.urls import path
from . import views

urlpatterns = [
    path('', views.slide_builder, name='slide_builder'),
    path('api/generate_slides/', views.generate_slides, name='generate_slides'),
    path('api/share/', views.share_slides, name='share_slides'),
    path('view/<str:code>/', views.view_shared, name='view_shared'),
]