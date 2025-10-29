from django import forms
from django.db import models
from .models import Note
from .forms import RegisterForm , LoginForm
from django.contrib.auth.mixins import LoginRequiredMixin   
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import NoteForm 

class NoteListView(LoginRequiredMixin, ListView):
    model= Note
    template_name = 'note_list.html'
    context_object_name = 'notes'
    paginate_by = 10
    def get_queryset(self):
        return Note.objects.filter(user=self.request.user).order_by('-created_at')
class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    # fields = ['title', 'content']
    form_class = NoteForm
    template_name = 'note_form.html'
    success_url = reverse_lazy('note_list')
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Note created successfully.")
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'ADD NOTE'
        context['button_text'] = 'Save'
        return context
class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    # fields = ['title', 'content']
    form_class = NoteForm
    template_name = 'note_form.html'
    success_url = reverse_lazy('note_list')
    def form_valid(self, form):
        messages.success(self.request, "Note updated successfully.")
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'EDIT NOTE'
        context['button_text'] = 'Save'
        return context
    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)
class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    success_url = reverse_lazy('note_list')

    def get_queryset(self):
        # Make sure users can delete only their own notes
        return Note.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        """
        Skip the default confirmation template and delete immediately.
        """
        note = self.get_object()
        note.delete()
        messages.success(request, "Note deleted successfully.")
        return redirect(self.success_url)

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please log in.")
            messages.error(request, "Please enter valid details.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('note_list')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    messages.error(request, 'Enter Valid Username/Password.' )
    return redirect('login')
