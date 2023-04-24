from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserForm, ProfileForm, AddImageForm
from .models import Profile, AddImage
from django.views.generic import DetailView, UpdateView, DeleteView, ListView, CreateView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from taggit.models import Tag 
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from dev.models import Startup, Team
from utopies.models import Utopies
from itutopies.models import ITUtopies


@login_required
def like_view(request, pk):
    profile = get_object_or_404(Profile, id=request.POST.get('profile_id'))
    liked = False
    if profile.raiting.filter(id=request.user.id).exists():
        profile.raiting.remove(request.user)
        liked = False
    else:
        profile.raiting.add(request.user)
        liked = True

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class GetProfile(DetailView):
    model = Profile
    template_name = 'regauth/account.html'

 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = get_object_or_404(Profile, slug=self.kwargs.get('slug'))
        total_raiting = profile.total_raiting()
        images = AddImage.objects.filter(author=profile.user).order_by('-date')
        itutopies = ITUtopies.objects.filter(author=profile.user).order_by('-date')
        utopies = Utopies.objects.filter(author=profile.user).order_by('-date')
        startups = Startup.objects.filter(founder=profile.user).order_by('-date')

        team = Team.objects.filter(participants=profile.user)

        raiting = False
        if profile.raiting.filter(id=self.request.user.id).exists():
            raiting = True

        context['utopies'] = utopies
        context['itutopies'] = itutopies
        context['startups'] = startups
        context['team'] = team
        context['raiting'] = raiting
        context['total_raiting'] = total_raiting
        context['images'] = images
        return context


class SearchProfileResultsView(ListView):
    template_name = 'regauth/searchprofile.html'
 
    def get_queryset(self): 
        query = self.request.GET.get('q')

        object_list = Profile.objects.filter( 
            Q(bio__icontains=query) | Q(tags__name__icontains=query) | Q(user__username__icontains=query) | Q(user__last_name__icontains=query)  | Q(user__first_name__icontains=query)
        ).order_by('-id')

        return object_list


def ProfileTaggit(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    news = Profile.objects.filter(tags=tag)
 
    object_list = {
        'tag':tag,
        'news':news,
    }
    return render(request, 'regauth/searchprofile.html', object_list)

 
class ImageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = AddImage
    form_class = AddImageForm
    template_name = 'regauth/addimage.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class ImageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = AddImage
    template_name = 'utopies/utopia-delete.html'
    success_url = '/regauth/profile'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def regauth(request):
    if request.user.is_authenticated:
        return redirect('profile')

    form = UserRegisterForm()
    context = {'form': form}
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш аккаунт успешно создан!')
            return redirect('auth')
    return render(request, 'regauth/register.html', {'form': form})


def auth(request):
    form = UserRegisterForm()
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
       
        if user is not None:
            login(request, user)
            return redirect('auth')

    context = {'form': form}
    return render(request, 'regauth/auth.html', context)


def LogoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='auth')
def profile(request):
    itopia = ITUtopies.objects.order_by('-date')
    utopia = Utopies.objects.order_by('-date')
    images = AddImage.objects.order_by('-date')
    startups = Startup.objects.all()
    profile = Profile.objects.all()
    tags = Profile.tags.all()
    team = Team.objects.filter(participants=request.user)
    context = {
        'images': images,
        'startups': startups,
        'utopia': utopia,
        'itopia': itopia,
        'team': team,
        'tags': tags
    }


    return render(request, 'regauth/profile.html', context)

@login_required(login_url='auth')
def userform(request):
    profile = get_object_or_404(Profile,user=request.user)
    if request.method == 'POST':
        User_Form = UserForm(request.POST, instance=request.user)
        Profile_Form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if User_Form.is_valid() and Profile_Form.is_valid():
            User_Form.save()
            Profile_Form.save()
            messages.success(request, ('Ваш профиль был успешно обновлен!'))
            return redirect('profile')
        else:
            messages.error(request, ('Пожалуйста, исправьте ошибки.'))
    else:
        User_Form = UserForm(instance=request.user)
        Profile_Form = ProfileForm(instance=request.user.profile)

    return render(request, 'regauth/editprofile.html', {
        'User_Form': User_Form,
        'Profile_Form': Profile_Form
    })

class ImageCreateView(CreateView):
    model = AddImage
    form_class = AddImageForm
    template_name = 'regauth/addimage.html'

    def form_valid(self, form):
        image = form.save(commit=False)
        image.author = self.request.user
        image.save()
        return super().form_valid(form)


    def get_queryset(self):
        profile = Profile.objects.all()
        return profile