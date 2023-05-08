from .dataclasses import FlashMessages
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import ProtectedError


class UserChangeAccessMixin:

    redirect_field_name = None

    def has_permission(self) -> bool:
        return self.get_object().pk == self.request.user.pk

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request,
                FlashMessages.NO_AUTHENTICATION.value,
            )

            return self.handle_no_permission()

        elif not self.has_permission():
            messages.error(
                request,
                FlashMessages.NO_PERMIT_TO_CHANGE_USER.value,
            )
            return redirect('users')
        return super().dispatch(request, *args, **kwargs)


class UserDeleteAccessMixin(UserChangeAccessMixin):

    def form_valid(self, form):
        try:
            self.object.delete()
            messages.success(
                self.request, FlashMessages.USER_SUCCESSFULLY_DELETE.value
            )
            return redirect('users')

        except ProtectedError:
            messages.error(self.request,
                           FlashMessages.USER_IS_USING.value)
            return redirect('users')


class PermissionMixin:
    redirect_field_name = None

    def has_permission(self) -> bool:
        return self.get_object().creator.pk == self.request.user.pk

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                self.request, FlashMessages.NO_AUTHENTICATION.value
            )
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
