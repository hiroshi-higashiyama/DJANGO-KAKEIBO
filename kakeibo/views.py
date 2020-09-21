from django.shortcuts import render
from .forms import KakeiboForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import Category, Kakeibo
from django.db import models
import calendar
from django.db.models import Sum


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


def show_line_grahp(request):
    kakeibo_data = Kakeibo.objects.all()

    category_list = []
    category_data = Category.objects.all().order_by('-category_name')
    for item in category_data:
        category_list.append(item.category_name)

    date_list = []
    for i in kakeibo_data:
        date_list.append(i.date.strftime('%Y/%m/%d')[:7])

    # 重複値の除外
    x_label = list(set(date_list))
    x_label.sort(reverse=False)

    # 月毎＆カテゴリ毎の合計金額データセットの生成
    monthly_sum_data = []
    for i in range(len(x_label)):
        year, month = x_label[i].split("/")
        month_range = calendar.monthrange(int(year), int(month))[1]
        first_date = year + '-' + month + '-' + '01'
        last_date = year + '-' + month + '-' + str(month_range)
        # １か月分データを取得
        total_of_month = Kakeibo.objects.filter(date__range=(first_date, last_date))
        category_total = total_of_month.values('category').annotate(total_price=Sum('money'))

        for j in range(len(category_total)):
            money = category_total[j]['total_price']
            category = Category.objects.get(pk=category_total[j]['category'])
            monthly_sum_data.append([x_label[i], category.category_name, money])

    # 折れ線グラフのボーダーカラー色の設定
    border_color_list = ['254,97,132,0.8', '54,164,235,0.8', '0,255,65,0.8', '255,241,15,0.8',
                         '255,94,25,0.8', '84,77,203,0.8', '204,153,50,0.8', '214,216,165,0.8',
                         '33,30,45,0.8', '52,38,89,0.8']
    border_color = []
    for x, y in zip(category_list, border_color_list):
        border_color.append([x, y])

    background_color_list = ['254,97,132,0.5', '54,164,235,0.5', '0,255,65,0.5', '255,241,15,0.5',
                             '255,94,25,0.5', '84,77,203,0.5', '204,153,50,0.5', '214,216,165,0.5',
                             '33,30,45,0.5', '52,38,89,0.5']

    background_color = []
    for x, y in zip(category_list, background_color_list):
        background_color.append([x, y])

    # 月毎＆カテゴリ毎の合計金額データを生成する。
    # カテゴリが登録されていない月の合計金額は０にセットする。
    # まず、全日付ｘ全カテゴリｘ合計金額「0]のリストを生成する。
    matrix_list = []
    for item_label in x_label:
        for item_category in category_list:
            matrix_list.append([item_label, item_category, 0])

    """matrix_listとmonthlysum_dataに対して、「年月+カテゴリ」の
    組み合わせが一致する要素に対してmatrix_listの金額（０円）を
    monthly_sum_dataの金額で上書きする。
    """
    for yyy_mm, category, total in monthly_sum_data:
        for i, data in enumerate(matrix_list):
            if data[0] == yyy_mm and data[1] == category:
                matrix_list[i][2] = total

    return render(request, 'kakeibo/kakeibo_line.html', {
        'x_label': x_label,
        'category_list': category_list,
        'border_color': border_color,
        'background_color': background_color,
        'matrix_list': matrix_list,
    })
