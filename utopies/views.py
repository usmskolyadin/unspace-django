from django.shortcuts import render, redirect, get_object_or_404
from .models import Utopies, UtopiaComment
from django.contrib.auth.decorators import login_required
from .forms import UtopiesForm, UtopiaCommentForm
from django.views.generic import DetailView, UpdateView, DeleteView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from regauth.models import Profile
from taggit.models import Tag
from pytils.translit import slugify
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect


def utopies(request):
    news = Utopies.objects.order_by('-date')

    return render(request, 'utopies/utopies.html', {'news': news})

def UtopiaTaggit(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    news = Utopies.objects.filter(tags=tag)
    
    context = {
        'tag': tag,
        'news': news,
    }
    return render(request, 'utopies/utopies.html', context)


class UtopiaView(DetailView):
    model = Utopies
    template_name = 'utopies/utopia.html'
    context_object_name = 'Utopia'
    query_pk_and_slug = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        stuff = get_object_or_404(Utopies, slug=self.kwargs['slug'])

        total_likes = stuff.total_likes()

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context['total_likes'] = total_likes
        context['liked'] = liked
        return context


class AddUtopiaComment(CreateView):
    model = UtopiaComment
    form_class = UtopiaCommentForm
    template_name = 'utopies/addcomment.html'

    def form_valid(self, form):
        form.instance.utopia = Utopies.objects.get(slug=self.kwargs['slug'])
        comments = form.save(commit=False)
        comments.author = self.request.user
        comments.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('utopia', kwargs={'pk': self.object.utopia.id, 'slug': self.object.utopia.slug})


class UtopiaEditComment(UpdateView):
    model = UtopiaComment
    form_class = UtopiaCommentForm
    template_name = 'utopies/addcomment.html'

    def get_success_url(self):
        return reverse('utopia', kwargs={'pk': self.object.utopia.id, 'slug': self.object.utopia.slug})


class UtopiaDeleteComment(DeleteView):
    model = UtopiaComment
    template_name = 'utopies/utopia-delete.html'

    def get_success_url(self):
        return reverse('utopia', kwargs={'pk': self.object.utopia.id, 'slug': self.object.utopia.slug})


class UserUtopiesListView(ListView):
    model = Utopies
    template_name = 'utopies/user-utopies.html'
    context_object_name = 'Utopia'
    paginate_by = 5


    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Utopies.objects.filter(author=user).order_by('-likes')


def pageNotFound(request, exception):
    return render(request, 'utopies/fournullfour.html')


class UtopiaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Utopies
    form_class = UtopiesForm
    template_name = 'utopies/utopiaform.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


@login_required
def like_view(request, pk):
    utopia = get_object_or_404(Utopies, id=request.POST.get('utopia_id'))
    liked = False
    if utopia.likes.filter(id=request.user.id).exists():
        utopia.likes.remove(request.user)
        liked = False
    else:
        utopia.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class UtopiaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Utopies
    template_name = 'utopies/utopia-delete.html'
    success_url = '/utopies/'

 
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class UtopiaCreateView(LoginRequiredMixin, CreateView):
    model = Utopies
    form_class = UtopiesForm
    template_name = 'utopies/utopiaform.html'
    login_url = 'auth'

    def form_valid(self, form):
        utopies = form.save(commit=False)
        utopies.author = self.request.user
        utopies.save()
        return super().form_valid(form)



def privatypolicy(request, tag_slug=None):
    news = Utopies.objects.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        news = news.filter(tags__in=[marketing])

    return render(request, 'utopies/privaty-policy.html', {'news': news, 'tag': tag})


def useragreement(request, tag_slug=None):
    news = Utopies.objects.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        news = news.filter(tags__in=[tag])

    return render(request, 'utopies/user-agreement.html', {'news': news})


def coding(request, tag_slug=None):
    news = Utopies.objects.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        news = news.filter(tags__in=[tag])

    return render(request, 'utopies/coding.html', {'news': news})


def marketing(request, tag_slug=None):
    news = Utopies.objects.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        news = news.filter(tags__in=[tag])

    return render(request, 'utopies/marketing.html', {'news': news})


def about(request, tag_slug=None):
    news = Utopies.objects.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        news = news.filter(tags__in=[tag])

    return render(request, 'utopies/about.html', {'news': news})


def design(request, tag_slug=None):
    news = Utopies.objects.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        news = news.filter(tags__in=[tag])

    return render(request, 'utopies/design.html', {'news': news})


def neirone(request, tag_slug=None):
    news = Utopies.objects.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        news = news.filter(tags__in=[tag])

    return render(request, 'utopies/neirone.html', {'news': news})
