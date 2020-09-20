from django.urls import path
from .views import KakeiboListView, KakeiboCreateView, create_done, KakeiboUpdateView, update_done, KakeiboDeleteView, delete_done, show_circle_grahp

app_name = 'kakeibo'

urlpatterns = [
    path('kakeibo_list/', KakeiboListView.as_view(), name='kakeibo_list'),
    path('kakeibo_create/', KakeiboCreateView.as_view(), name='kakeibo_create'),
    path('create_done/', create_done, name='create_done'),
    path('update/<int:pk>', KakeiboUpdateView.as_view(), name='kakeibo_update'),
    path('update_done/', update_done, name='update_done'),
    path('delete/<int:pk>/', KakeiboDeleteView.as_view(), name='kakeibo_delete'),
    path('delete_done/', delete_done, name='delete_done'),
    path('circle/', show_circle_grahp, name='kakeibo_circle'),
]
