from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView, TemplateView
from django.db.models import Q
from django.urls import reverse_lazy

from .models import DiaryEntry
from .forms import DiaryEntryForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .permissions import OwnerRequiredMixin
from users.permissions import ActiveUserMixin


class DiaryBaseView(ActiveUserMixin):
    '''Базовый для views, приватность, фильтрация по владельцу'''
    model = DiaryEntry

    def get_queryset(self):
        return DiaryEntry.objects.filter(author=self.request.user)


class HomeView(TemplateView):
    template_name = 'diary/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and self.request.user.is_active:
            # Для авторизованных можно показать последние записи
            context['recent_entries'] = DiaryEntry.objects.filter(
                author=self.request.user
            ).order_by('-created_at')[:3]
        return context


class CreateDiaryView(DiaryBaseView, CreateView):
    '''Создание записи'''
    form_class = DiaryEntryForm
    template_name = 'diary/form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    success_url = reverse_lazy('diary:diary_list')


class DiaryListView(DiaryBaseView, ListView):
    '''Мои записи'''
    template_name = 'diary/diary_list.html'
    context_object_name = 'diary_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        if search_query:
            return queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query)
            )
        return queryset


class DiaryDetailView(DiaryBaseView, OwnerRequiredMixin, DetailView):
    '''Инфо личной записи'''
    template_name = 'diary/diary_detail.html'
    context_object_name = 'diary_entry'


class DiaryDeleteView(DiaryBaseView, OwnerRequiredMixin, DeleteView):
    '''Удаление записи'''
    template_name = 'diary/confirm_delete.html'
    success_url = reverse_lazy('diary:diary_list')


class DiaryUpdateView(DiaryBaseView, OwnerRequiredMixin, UpdateView):
    '''Изменения записи'''
    template_name = 'diary/form.html'
    form_class = DiaryEntryForm
    success_url = reverse_lazy('diary:diary_list')
