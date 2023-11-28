from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'display/index.html')


def about(request):
    return render(request, 'display/about.html')


def solutions(request):
    return render(request, 'display/solutions.html')