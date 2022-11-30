from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='polls_list'),
    path('<int:id>/details/', views.details, name="poll_details"),
    path('<int:id>/', views.poll, name="single_poll"),
    path('add_poll/', views.add_poll, name='add_poll'), # my own code
    path('add_choice/', views.add_choice, name="add_choice"), # my own code
    path('add/', views.PollView.as_view(), name="poll_add"),
    path('<int:id>/edit/', views.PollView.as_view(), name="poll_edit"), # sir code
    path('<int:id>/delete/', views.PollView.as_view(), name="poll_delete"), #sir code
]