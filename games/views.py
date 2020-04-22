from django.shortcuts import render
from django.http import HttpResponse
from .forms import ButtonForm

def root(request):
    context={}
    print("in root")
    return render(request, 'root/root.html', context)
    #return HttpResponse("Hello, world.")


