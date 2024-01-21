from django.shortcuts import render, redirect


def home(request):
    return render(request=request, template_name='index.html')


def index(request):
    if request.user.is_authenticated:
        return redirect('/home/')
    else:
        return redirect('/accounts/login/')
