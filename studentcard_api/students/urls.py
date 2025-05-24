from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student-list'),
    path('add/', views.student_form, name='student-form'),
    path('delete/<int:pk>/', views.student_delete, name='student-delete'),

]