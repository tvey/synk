from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    View,
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy

from .forms import LinkForm, LinkModelForm
from .models import Link
from .utils import decode_link


class HomeView(View):
    template_name = 'shortener/index.html'
    form_class = LinkForm
    success_url = reverse_lazy('result')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = {'form': form}
        request.session['source'] = form.data['source']
        if form.is_valid():
            source = form.cleaned_data.get('source')
            owner = request.user if request.user.is_authenticated else None
            link, created = Link.objects.get_or_create(source=source, owner=owner)
            request.session['code'] = link.code
            if owner and not created:
                request.session['exists'] = True
            else:
                request.session['exists'] = False
            return redirect(self.success_url)

        return render(request, self.template_name, context)


class ResultView(View):
    template_name = 'shortener/result.html'
    form_class = LinkForm

    def get(self, request, *args, **kwargs):
        link = get_object_or_404(Link, code=request.session.get('code'))
        domain = request.get_host()
        result = f'{domain}/{link.code}/'
        form = self.form_class(initial={'source': result})
        context = {'form': form, 'result': result}
        source = request.session.get('source')
        context['source'] = decode_link(source)
        context['exists'] = request.session.get('exists')
        return render(request, self.template_name, context)


class LinkRedirectView(View):
    def get(self, request, code=None, *args, **kwargs):
        link = get_object_or_404(Link, code=code)
        link.click_set.create()
        return redirect(link.source)


class DashboardView(LoginRequiredMixin, ListView):
    model = Link
    template_name = 'shortener/dashboard.html'
    context_object_name = 'link_list'
    paginate_by = 15

    def get_queryset(self, *args, **kwargs):
        owner = self.request.user
        return Link.objects.filter(owner=owner).order_by('-updated')


class SearchView(ListView):
    template_name = 'shortener/dashboard.html'
    context_object_name = 'link_list'

    def get_queryset(self):
        q = self.request.GET.get('q')
        user_links = Link.objects.filter(owner=self.request.user)
        qs = user_links.filter(
            Q(name__icontains=q) | Q(code__icontains=q) | Q(source__icontains=q)
        )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context


class LinkCreateView(LoginRequiredMixin, CreateView):
    form_class = LinkModelForm
    success_url = reverse_lazy('dashboard')
    template_name = 'shortener/link_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class LinkUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    success_url = reverse_lazy('dashboard')
    form_class = LinkModelForm

    def test_func(self):
        link = self.get_object()
        if self.request.user == link.owner:
            return True
        return False

    def get_object(self):
        return get_object_or_404(Link, code=self.kwargs['code'])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class LinkDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Link
    success_url = reverse_lazy('dashboard')

    def test_func(self):
        link = self.get_object()
        if self.request.user == link.owner:
            return True
        return False

    def get_object(self):
        return get_object_or_404(Link, code=self.kwargs['code'])


class AboutView(TemplateView):
    template_name = "shortener/about.html"
