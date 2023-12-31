from django.shortcuts import render, get_object_or_404, redirect 
import random 
from random import sample 
from . models import GenPass 
from django.contrib import messages

# Create your views here.
def home(request):
    if request.method == "POST":
        site = request.POST.get('site')
        length = request.POST.get('length') 
        if site == "" or length == "":
            n= 'incorrect input Please write Something'
            messages.success(request,n)
            return render(request, 'generator/home.html')
        if not length.isdigit():
            n = "invalid inputs Of Length" 
            messages.success(request, n)
            return render(request, 'generator/home.html')
        password_length = int(request.POST.get('length'))
        characters = "!@#$%^&**()_+"
        numbers = '1234567890'
        small_letters = "qwertyuioplkjhgfdsazxcvbnm"
        upper_case = "QWERTYUIOPASDFGHJKLMNBVCXZ"
        prep = characters + numbers + small_letters + upper_case
        if password_length > 30:
            # message = "can't generate password more than 30 characters"
            # context = {
            #     'message':message
            # }
            n = "can't generate password more than 30 characters"
            messages.success(request,n)
            return render(request, 'generator/home.html')
        
        else:
            passwd = ''.join(random.sample(prep, k=password_length))
            print(passwd)
            p = GenPass.objects.create(site=site, password=passwd)
            p.save()

            context = {
                'password':passwd
            }
            return render(request, 'generator/success.html',context)
    return render(request, "generator/home.html")


def listall(request):
    context = {
        'items':GenPass.objects.all()
    }
    return render(request, 'generator/listall.html',context)


def search(request):
    if request.method == "POST":
        query = request.POST.get('site',None)
        if query:
            results = GenPass.objects.filter(site__contains=query)
            return render(request, 'generator/search.html',{'results':results})
    return render(request, 'generator/search.html')


def deleterecord(request,id):
    obj = get_object_or_404(GenPass, id=id)
    obj.delete()
    return redirect('listall')

