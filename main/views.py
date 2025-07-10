import logging
import sys
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, CreateView
import math  # use in CalcPage
from main.forms import CalcForm, CreateNoteForm, FindNoteForm
from main.import_checkers import BlockElevateImporter
from main.models import Note

logger = logging.getLogger('custom_django')


class IndexPage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        return context


class CreateNotePage(LoginRequiredMixin, CreateView):
    form_class = CreateNoteForm
    model = Note

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'id': self.request.user.id})

    def get_initial(self):
        initial = super().get_initial()
        initial['author_id'] = self.request.user.id
        return initial


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
        form = CreateNoteForm(initial={'author': self.request.user})
        context['form'] = form
        if self.object == self.request.user:
            context['notes'] = Note.get_all_notes_of_user(self.object)
        else:
            context['notes'] = Note.get_open_notes_of_user(self.object)
        return context


class NotePage(LoginRequiredMixin, DetailView):
    template_name = 'note.html'
    model = Note

    def get_object(self, queryset=None):
        return get_object_or_404(Note, id=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        if self.object.author != self.request.user and not self.object.is_open:
            raise Http404()
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        context['text'] = self.object.text
        context['is_open'] = self.object.is_open
        context['author'] = self.object.author
        return context


class NotesPage(LoginRequiredMixin, TemplateView):
    template_name = 'notes.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        form = FindNoteForm(request.POST)
        if form.is_valid():
            text = form.data['text']
            if text:
                context['notes'] = Note.sql_find_by_text(text)
                # context['notes'] = Note.find_by_text(text)
            else:
                context['notes'] = Note.get_open_notes()
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Заметки'
        context['notes'] = Note.get_open_notes()
        context['form'] = FindNoteForm()
        return context


class CalcPage(TemplateView):
    template_name = 'calc.html'

    def get_context_data(self, **kwargs):
        sys.meta_path.insert(0, BlockElevateImporter())
        context = super().get_context_data(**kwargs)
        context['title'] = 'Калькулятор'
        context['form'] = CalcForm()
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        form = CalcForm(request.POST)
        if form.is_valid():
            expression = form.data['expression']
            try:
                if 'rm' in expression:
                    print('rm detected')
                    raise ValueError
                context['result'] = eval(expression)
            except ValueError:
                context['result'] = 'Ошибка во время подсчёта...'
        return render(request, self.template_name, context)


class SecretPage(TemplateView):
    template_name = 'secret.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Секретная страница'
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        if request.headers.get('algorithm') == 'PBKDF2':
            context['text'] = 'Правильно! Флаг: mshp{supp3r_dup3r_secr3t}'
        else:
            context['text'] = 'Какой алгоритм хеширования использует django? В ответе только одно слово.'
        return render(request, self.template_name, context)


def logout_view(request):
    logger.info('%s logged out', request.user.username)
    logout(request)
    return redirect('index')
