from django.core.exceptions import PermissionDenied


class OwnerRequiredMixin:
    '''Проверка владельца записи'''
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user:
            raise PermissionDenied('У Вас нет доступа к этой записи, так как Вы не являетесь ее владельцем')
        return super().dispatch(request, *args, **kwargs)


class UserFilterMixin:
    '''Фильтрация по владельцу'''
    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)