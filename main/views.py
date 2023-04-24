from django.shortcuts import render
from .models import GlavProfile
from utopies.models import Utopies
from itutopies.models import ITUtopies
from regauth.models import AddImage
from .models import News
from django.db.models import Q
from django.views.generic import DetailView, UpdateView, DeleteView, ListView, CreateView
from taggit.models import Tag 
import requests
from dev.models import Startup

def index(request):
    minititle = GlavProfile.objects.all()
    context = {
        "minititle": minititle
    }
    return render(request, 'main/index.html', context)



def unews(request):
    utopies = Utopies.objects.filter().order_by('-id')[:3]
    itutopies = ITUtopies.objects.filter().order_by('-id')[:3]
    images = AddImage.objects.filter().order_by('-id')[:6]
    news = News.objects.all()
    startups = Startup.objects.filter().order_by('-id')[:1]

    context = {
        "utopies": utopies,
        "itutopies": itutopies,
        "images": images,
        "news": news,
        "startups": startups
    }

    return render(request, 'main/unews.html', context)


class SearchResultsView(ListView):
    template_name = 'utopies/results.html'
 
    def get_queryset(self): 
        query = self.request.GET.get('q')

        object_list = Utopies.objects.filter( 
            Q(title__iregex=query) | Q(full_text__iregex=query) | Q(author__username__icontains=query) | Q(tags__name__icontains=query) | Q(project__iregex=query)
        ).order_by('-date')

        return object_list