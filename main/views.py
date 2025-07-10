import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.views.generic import TemplateView, DetailView
import math

from main.forms import CalcForm

logger = logging.getLogger('custom_django')


class IndexPage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        return context


class ProfilePage(LoginRequiredMixin, DetailView):
    template_name = 'profile.html'
    model = User

    def get_object(self, queryset=None):
        return get_object_or_404(User, id=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Профиль'
        if self.object.username == 'admin':
            context['flag'] = 'mshp{n0w_1_am_aDmIn}'
        else:
            context['flag'] = 'mshp{really?}'
        return context


class CalcPage(TemplateView):
    template_name = 'calc.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Калькулятор'
        context['form'] = CalcForm()
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        form = CalcForm(request.POST)
        if form.is_valid():
            try:
                context['result'] = eval(form.data['expression'])
            except ValueError:
                context['result'] = 'Ошибка во время подсчёта...'
        return render(request, self.template_name, context)


def logout_view(request):
    logger.info('%s logged out', request.user.username)
    logout(request)
    return redirect('index')
