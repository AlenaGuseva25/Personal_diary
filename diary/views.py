from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from django.db.models import Q
from django.urls import reverse_lazy
from .models import DiaryEntry
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import OwnerRequiredMixin, UserFilterMixin


class DiaryBaseView(LoginRequiredMixin):
    '''Базовый для views, приватность'''
    model = DiaryEntry
    raise_exception = True

    def get_queryset(self):
        return DiaryEntry.objects.filter(owner=self.request.user)


class CreateDiaryView(LoginRequiredMixin, CreateView):
    '''Создание записи'''
    model = DiaryEntry
    fields = ['title', 'content', 'picture']
    template_name = 'diary/form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    success_url = reverse_lazy('diary-list')


class DiaryListView(UserFilterMixin, ListView):
    '''Мои записи'''
    template_name = 'diary/list.html'
    context_object_name = 'diary_entries'
    paginate_by = 10
    ordering = ('-created_at',)

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
    template_name = 'diary/detail.html'
    context_object_name = 'diary_entry'


class DiaryDeleteView(DiaryBaseView, OwnerRequiredMixin, DeleteView):
    '''Удаление записи'''
    template_name = 'diary/confirm_delete.html'
    success_url = reverse_lazy('diary-list')


class DiaryUpdateView(DiaryBaseView, OwnerRequiredMixin, UpdateView):
    '''Изменения записи'''
    template_name = 'diary/form.html'
    fields = ['title', 'content', 'picture']
    success_url = reverse_lazy('diary-list')
