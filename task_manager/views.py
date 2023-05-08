from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .dataclasses import FlashMessages


def main_page(request: HttpRequest) -> HttpResponse:
    return render(request, 'base.html')


class Login(SuccessMessageMixin,
            LoginView,
            ):

    form_class = AuthenticationForm
    template_name = 'login.html'
    success_message = FlashMessages.LOGIN_SUCCESS.value

    def get_success_url(self):
        return reverse_lazy('main_page')


def logout_user(request):
    logout(request)
    messages.success(request, FlashMessages.LOGOUT_SUCCESS.value)
    return redirect('main_page')
