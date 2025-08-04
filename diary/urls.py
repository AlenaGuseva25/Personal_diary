from django.urls import path
from .views import (
CreateDiaryView,
DiaryListView,
DiaryDetailView,
DiaryDeleteView,
DiaryUpdateView,
)


app_name = 'diary'

urlpatterns = [
    path('create/', CreateDiaryView.as_view(), name='create'),
    path('', DiaryListView.as_view(), name='list'),
    path('<int:pk>/', DiaryDetailView.as_view(), name='detail'),
    path('<int:pk>/delete/', DiaryDeleteView.as_view(), name='delete'),
    path('<int:pk>/update/', DiaryUpdateView.as_view(), name='update'),
]