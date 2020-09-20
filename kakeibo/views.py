from django.shortcuts import render
from .forms import KakeiboForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import Category, Kakeibo
from django.db import models


class KakeiboListView(ListView):
    model = Kakeibo
    template_name = 'kakeibo/kakeibo_list.html'
    context_object_name = 'kakeibo_list'

    def queryset(self):
        return Kakeibo.objects.all()


class KakeiboCreateView(CreateView):
    model = Kakeibo
    form_class = KakeiboForm
    template_name = 'kakeibo/kakeibo_form.html'
    success_url = reverse_lazy('kakeibo:create_done')


def create_done(request):
    return render(request, 'kakeibo/create_done.html')


class KakeiboUpdateView(UpdateView):
    model = Kakeibo
    form_class = KakeiboForm
    template_name = 'kakeibo/kakeibo_form.html'
    success_url = reverse_lazy('kakeibo:update_done')


def update_done(request):
    return render(request, 'kakeibo/update_done.html')


class KakeiboDeleteView(DeleteView):
    model = Kakeibo
    success_url = reverse_lazy('kakeibo:delete_done')


def delete_done(request):
    return render(request, 'kakeibo/delete_done.html')


def show_circle_grahp(request):
    # 合計金額
    kakeibo_data = Kakeibo.objects.all()

    total = 0
    for item in kakeibo_data:
        total += item.money

    # カテゴリごとの合計金額
    category_list = []
    category_data = Category.objects.all()
    for item in category_data:
        category_list.append(item.category_name)

    category_dict = {}  # カテゴリ別の割合を格納
    for i, item in enumerate(category_list):
        category_total = Kakeibo.objects.filter(category__category_name=category_list[i]).aggregate(sum=models.Sum('money'))['sum']
        # 割合を求める
        if category_total != None:
            ratio = int((category_total / total) * 100)
            category_dict[item] = ratio
        else:
            ratio = 0
            category_dict[item] = ratio

    return render(request, 'kakeibo/kakeibo_circle.html', {
        'category_dict': category_dict,
    })
