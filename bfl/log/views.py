from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Session


class SessionListView(ListView):
    model = Session
    ordering = '-date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'My Sessions'
        return context

    def get_queryset(self):
        queryset = Session.objects.filter(user=self.request.user)
        return queryset.order_by(self.ordering)


class SessionDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Session

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context

    def test_func(self):
        session = self.get_object()
        if self.request.user == session.user or self.request.user.is_superuser:
            return True
        return False


class SessionCreateView(LoginRequiredMixin, CreateView):
    model = Session
    fields = ['name']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New Session'
        context['page_title'] = 'New Workout Session'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SessionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Session
    fields = ['name']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit ' + self.object.name
        context['page_title'] = self.object.name
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        session = self.get_object()
        if self.request.user == session.user or self.request.user.is_superuser:
            return True
        return False


class SessionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Session
    success_url = '/sessions/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete ' + self.object.name
        return context

    def test_func(self):
        session = self.get_object()
        if self.request.user == session.user or self.request.user.is_superuser:
            return True
        return False

