from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from .models import Category, Kakeibo


class KakeiboListView(ListView):
    model = Kakeibo
    template_name = 'kakeibo/kakeibo_list.html'
    context_object_name = 'kakeibo_list'

    def queryset(self):
        return Kakeibo.objects.all()
