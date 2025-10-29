from django import forms
from django.db import models
from .models import Note
from django.urls import path
from .views import NoteCreateView, NoteUpdateView, NoteDeleteView, NoteListView
from .views import register_view, login_view, logout_view
urlpatterns = [
    path('', NoteListView.as_view(), name='note_list'),
    path('note/add/', NoteCreateView.as_view(), name='note_add'),
    path('note/<int:pk>/edit/', NoteUpdateView.as_view(), name='note_edit'),
    path('note/<int:pk>/delete/', NoteDeleteView.as_view(), name='note_delete'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
