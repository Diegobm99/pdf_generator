from django.urls import path
from post_api import views

urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),
    path('csv/', views.CSV.as_view())
]
