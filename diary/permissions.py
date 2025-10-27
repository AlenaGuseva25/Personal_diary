from django.core.exceptions import PermissionDenied


class OwnerRequiredMixin:
    '''Проверка, что пользователь == Владелец записи'''
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            raise PermissionDenied('У Вас нет доступа к этой записи, так как Вы не являетесь ее владельцем')
        return super().dispatch(request, *args, **kwargs)
