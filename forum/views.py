from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from .models import Forum


class OwnerProtectMixin(object):
    def dispatch(self, request, *args, **kwargs):
        objectUser = self.get_object()
        if objectUser.user != self.request.user:
            return HttpResponseForbidden()
        return super(OwnerProtectMixin, self).dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')  # Protected the class
class ForumView(ListView):
    model = Forum
    context_object_name = "forums"
    queryset = Forum.objects.order_by('-created_at')


@method_decorator(login_required, name='dispatch')  # Protected the class
class ForumCreate(CreateView):
    model = Forum
    fields = ['title', 'desc']
    # widget = {'desc': forms.RadioSelect()}
    success_url = reverse_lazy('forum')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')  # Protected the class
class ForumUpdateView(OwnerProtectMixin, UpdateView):
    model = Forum
    fields = ['title', 'desc']
    context_object_name = 'forums'
    template_name = 'forum/forum_update_form.html'
    success_url = reverse_lazy('forum')


@method_decorator(login_required, name='dispatch')  # Protected the class
class ForumDetailView(DetailView):
    model = Forum
    context_object_name = 'forums'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['additional'] = 'this is the value of the additional variable'
        return context


@method_decorator(login_required, name='dispatch')  # Protected the class
class ForumUserListView(ListView):
    context_object_name = "forums"  # has to be context of everything :)

    def get_queryset(self):
        self.user = get_object_or_404(User, username=self.kwargs['username'])
        print(self.user)
        print(Forum.objects.filter(user=self.user))
        return Forum.objects.filter(user=self.user)


