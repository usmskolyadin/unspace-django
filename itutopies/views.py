from django.shortcuts import render, redirect, get_object_or_404
from .models import ITUtopies, ITUtopiaComment
from django.contrib.auth.decorators import login_required
from .forms import ITUtopiesForm, ITUtopiaCommentForm
from django.views.generic import DetailView, UpdateView, DeleteView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from taggit.models import Tag
from regauth.models import Profile
from django.contrib import messages
from pytils.translit import slugify
from django.db.models import Q
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect


@login_required
def itlike_view(request, pk):
    itopia = get_object_or_404(ITUtopies, id=request.POST.get('itopia_id'))
    liked = False
    if itopia.likes.filter(id=request.user.id).exists():
        itopia.likes.remove(request.user)
        liked = False
    else:
        itopia.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def itsearch(request):
    object_list = ITUtopies.objects.order_by('-date')
    return render(request, 'itutopies/resultsit.html', {'object_list': object_list})


def itutopies(request):
    news = ITUtopies.objects.order_by('-date')
    paginator = Paginator(news, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'itutopies/itutopies.html', {'news': news, 'page_obj': page_obj, })


def ITUtopiaTaggit(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    news = ITUtopies.objects.filter(tags=tag)

    context = {
        'tag': tag,
        'news': news,
    }
    return render(request, 'itutopies/itutopies.html', context)


class SearchResultsViewIT(ListView):
    template_name = 'itutopies/resultsit.html'

    def get_queryset(self):
        query = self.request.GET.get('q')

        object_list = ITUtopies.objects.filter(
            Q(title__iregex=query) | Q(full_text__iregex=query) | Q(author__username__icontains=query) | Q(
                tags__name__icontains=query) | Q(code__iregex=query) | Q(project__iregex=query)
        ).order_by('-date')

        return object_list


class ITUtopiaView(DetailView):
    model = ITUtopies
    template_name = 'itutopies/itopia.html'
    context_object_name = 'Itopia'
    allow_empty = False
    query_pk_and_slug = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        stuff = get_object_or_404(ITUtopies, id=self.kwargs['pk'])

        total_likes = stuff.total_likes()

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context['total_likes'] = total_likes
        context['liked'] = liked
        return context


class UserITUtopiesListView(ListView):
    model = ITUtopies
    template_name = 'itutopies/user-itutopies.html'
    context_object_name = 'Itopia'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return ITUtopies.objects.filter(author=user).order_by('-date')


class ItopiaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ITUtopies
    form_class = ITUtopiesForm
    template_name = 'itutopies/itutopiaform.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class ItopiaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ITUtopies
    template_name = 'itutopies/itopia-delete.html'
    success_url = '/itutopies/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class ITUtopiaCreateView(LoginRequiredMixin, CreateView):
    model = ITUtopies
    form_class = ITUtopiesForm
    template_name = 'itutopies/itutopiaform.html'
    login_url = 'auth'

    def form_valid(self, form):
        itutopies = form.save(commit=False)
        itutopies.author = self.request.user
        itutopies.save()
        return super().form_valid(form)


class AddITUtopiaComment(CreateView):
    model = ITUtopiaComment
    form_class = ITUtopiaCommentForm
    template_name = 'itutopies/itcommentform.html'

    def form_valid(self, form):
        form.instance.itopia = ITUtopies.objects.get(slug=self.kwargs['slug'])
        comments = form.save(commit=False)
        comments.author = self.request.user
        comments.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('itopia', kwargs={'pk': self.object.itopia.id, 'slug': self.object.itopia.slug})


class ITUtopiaEditComment(UpdateView):
    model = ITUtopiaComment
    form_class = ITUtopiaCommentForm
    template_name = 'itutopies/itcommentform.html'

    def get_success_url(self):
        return reverse('itopia', kwargs={'pk': self.object.itopia.id, 'slug': self.object.itopia.slug})


class ITUtopiaDeleteComment(DeleteView):
    model = ITUtopiaComment
    template_name = 'utopies/utopia-delete.html'

    def get_success_url(self):
        return reverse('itopia', kwargs={'pk': self.object.itopia.id, 'slug': self.object.itopia.slug})
