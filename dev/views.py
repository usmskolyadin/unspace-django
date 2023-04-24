from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, UpdateView, DeleteView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from regauth.models import Profile
from taggit.models import Tag
from django.contrib import messages
from pytils.translit import slugify
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Startup
from .forms import StartupForm
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import StartupSerializer
from .models import Team
from .forms import TeamForm
from django.db.models import Q


class SearchStartupResultsView(ListView):
    template_name = 'dev/searchstar.html'
 
    def get_queryset(self): 
        query = self.request.GET.get('s')

        object_list = Startup.objects.filter( 
            Q(title__icontains=query) | Q(founder__username__icontains=query) | Q(founder__last_name__icontains=query)  | Q(founder__first_name__icontains=query) | Q(discription__icontains=query)
        ).order_by('-id')

        return object_list



class StartupCreateView(LoginRequiredMixin, CreateView):
    model = Startup
    form_class = StartupForm
    template_name = 'dev/startupform.html'
    login_url = 'auth'

    def form_valid(self, form):
        form.instance.team = Team.objects.get(pk=self.kwargs['pk'])
        comments = form.save(commit=False)
        comments.founder = self.request.user
        comments.save()
        return super().form_valid(form)


def teamview(request, pk):
    team = Team.objects.get(id=pk)
    participants = team.participants.all()
    startups = Startup.objects.filter(team=team)

    if request.method == 'POST':
        room.participants.add(request.user)
        return redirect('team', pk=team.id)

    context = {'team': team, 'participants': participants, 'startups': startups}
    return render(request, 'dev/team.html', context)




class TeamCreateView(LoginRequiredMixin, CreateView):
    model = Team
    form_class = TeamForm
    template_name = 'dev/teamform.html'
    login_url = 'auth'

    def form_valid(self, form):
        comments = form.save(commit=False)
        comments.founder = self.request.user
        comments.save()
        return super().form_valid(form)


class TeamUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Team
    form_class = TeamForm
    template_name = 'dev/teamform.html'

    def form_valid(self, form):
        form.instance.founder = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.founder:
            return True
        return False


class TeamDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Team
    template_name = 'utopies/utopia-delete.html'
    success_url = 'team'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.founder:
            return True
        return False

class TeamUserView(ListView):
    model = Team
    template_name = 'dev/youstartups.html'
    context_object_name = 'Startup'
 

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Startup.objects.filter(founder=user).all()





def startups(request):
    startups = Startup.objects.all()

    return render(request, 'dev/startups.html', context={'startups': startups})

class StartupView(DetailView):
    model = Startup
    template_name = 'dev/getstartup.html'
    context_object_name = 'Startup'
    query_pk_and_slug = True

 
class StartupUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Startup
    form_class = StartupForm
    template_name = 'dev/startupform.html'

    def form_valid(self, form):
        form.instance.founder = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.founder:
            return True
        return False

class StartupDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Startup
    template_name = 'utopies/utopia-delete.html'
    success_url = 'startups'

    def form_valid(self, form):
        form.instance.founder = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.founder:
            return True
        return False

class StartupUserView(ListView):
    model = Startup
    template_name = 'dev/youstartups.html'
    context_object_name = 'Startup'
 

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Startup.objects.filter(founder=user).all()


@api_view(['GET'])
def ApiOwerView(request):
    api_urls = {
        'List': '/startups/',
        'Detail': '/startup/<int:pk>/<str:slug>/'
    }
    return Response(api_urls)


@api_view(['GET'])
def startupslist(request):
    startups = Startup.objects.all()
    serializer = StartupSerializer(startups, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def startupCreate(request):
    serializer = StartupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.date)

@api_view(['POST'])
def startupUpdate(request, pk):
    startups = Startup.objects.get(id=pk)
    serializer = StartupSerializer(instance=startups, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def startupDelete(request, pk):
    startups = Startup.objects.get(id=pk)
    startups.delete()

    return Response(redirect('api-owerview'))

@api_view(['GET'])
def startupDetail(request, pk):
    startups = Startup.objects.get(id=pk)
    serializer = StartupSerializer(startups, many=False)
    return Response(serializer.data)
