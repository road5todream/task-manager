from .forms import UserRegistrationForm
from .models import Users
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from task_manager.dataclasses import FlashMessages
from task_manager.services import UserChangeAccessMixin, UserDeleteAccessMixin
from django.urls import reverse_lazy


class UsersView(ListView):

    model = Users


class RegisterUser(SuccessMessageMixin,
                   CreateView
                   ):

    model = Users
    form_class = UserRegistrationForm
    template_name = 'users/create_user.html'
    success_url = '/login/'
    success_message = FlashMessages.REGISTER_SUCCESS.value


class UpdateUserView(UserChangeAccessMixin,
                     LoginRequiredMixin,
                     SuccessMessageMixin,
                     UpdateView,
                     ):
    model = Users
    form_class = UserRegistrationForm
    template_name = 'users/update_user.html'
    success_url = reverse_lazy('users')
    success_message = FlashMessages.USER_SUCCESSFULLY_CHANGED.value


class DeleteUserView(UserDeleteAccessMixin,
                     LoginRequiredMixin,
                     DeleteView
                     ):
    model = Users
    success_url = reverse_lazy('users')
    template_name = 'users/delete_user.html'
