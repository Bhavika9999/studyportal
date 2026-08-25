from django.urls import path
from . import views

urlpatterns = [
    # Landing & Authentication
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # Student Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Notes Management
    path('notes/', views.notes_list, name='notes'),
    path('notes/add/', views.notes_add, name='notes_add'),
    path('notes/edit/<int:id>/', views.notes_edit, name='notes_edit'),
    path('notes/delete/<int:id>/', views.notes_delete, name='notes_delete'),

    # Homework Management
    path('homework/', views.homework_list, name='homework'),
    path('homework/add/', views.homework_add, name='homework_add'),
    path('homework/edit/<int:id>/', views.homework_edit, name='homework_edit'),
    path('homework/toggle/<int:id>/', views.homework_toggle, name='homework_toggle'),
    path('homework/delete/<int:id>/', views.homework_delete, name='homework_delete'),

    # To-Do List
    path('todo/', views.todo_list, name='todo'),
    path('todo/add/', views.todo_add, name='todo_add'),
    path('todo/edit/<int:id>/', views.todo_edit, name='todo_edit'),
    path('todo/toggle/<int:id>/', views.todo_toggle, name='todo_toggle'),
    path('todo/delete/<int:id>/', views.todo_delete, name='todo_delete'),

    # Educational Tools & APIs
    path('youtube/', views.youtube_search_view, name='youtube'),
    path('wikipedia/', views.wikipedia_search_view, name='wikipedia'),
    path('dictionary/', views.dictionary_view, name='dictionary'),
    path('books/', views.books_search_view, name='books'),
    path('unit-converter/', views.unit_converter_view, name='unit_converter'),
]
