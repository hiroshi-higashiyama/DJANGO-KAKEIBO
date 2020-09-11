from django.urls import path
from .views import KakeiboListView

app_name = 'kakeibo'

urlpatterns = [
    path('kakeibo_list/', KakeiboListView.as_view(), name='kakeibo_list'),
]
