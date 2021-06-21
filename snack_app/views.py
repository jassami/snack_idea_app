from django.shortcuts import redirect, render, HttpResponse
from django.apps import apps
User = apps.get_model('login_app', 'User')
from .models import *
from django.contrib import messages
from django.db.models import Count
import bcrypt

def index(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context={
        'user': User.objects.get(id= request.session['user_id']),
        'snacks': Snack.objects.annotate(Count('liked_by')).order_by('-liked_by__count'),
    }    
    return render(request, "snacks.html", context)

def create(request):
    errors = Snack.objects.snack_validator(request.POST)
    request.session['send']= "create"
    if errors:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect('/snacks')
    else:
        this_user= User.objects.get(id= request.session['user_id'])
        this_snack= Snack.objects.create(title= request.POST['title'], desc= request.POST['desc'], creator= this_user)
        this_snack.liked_by.add(this_user)
        request.session['snack_id']= this_snack.id
        return redirect('/snacks')

def delete(request, snack_id):
    snack= Snack.objects.get(id= snack_id)
    if snack.creator.id == request.session['user_id']:
        snack.delete()
    return redirect('/snacks')

def snack(request, snack_id):
    context={
        'user': User.objects.get(id= request.session['user_id']),
        'snack': Snack.objects.get(id= snack_id),
    }
    return render(request, 'snack_info.html', context)

def users(request, user_id):
    context={
        'user': User.objects.get(id= user_id),
    }
    return render(request, 'creator.html', context)

def update(request):
    user= User.objects.get(id= request.session['user_id'])
    errors = User.objects.update_validator(request.POST, user)
    request.session['send']= "update"
    if errors:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect(f'/snacks/users/{user.id}')
    else:
        if request.POST['first_name'] != "":
            user.first_name = request.POST['first_name']
        if request.POST['last_name'] != "":
            user.last_name = request.POST['last_name']
        if request.POST['email'] != "" and request.POST['email'] != user.email:
            user.email = request.POST['email']
        if request.POST['new_password'] != "":
            pw_hash= bcrypt.hashpw(request.POST['new_password'].encode(), bcrypt.gensalt()).decode()
            user.password = pw_hash
        user.save()
        return redirect(f'/snacks/users/{user.id}')

def like(request, snack_id):
    snack= Snack.objects.get(id= snack_id)
    user= User.objects.get(id= request.session['user_id'])
    snack.liked_by.add(user)
    snack.disliked_by.remove(user)
    return redirect(f'/snacks/{snack.id}')

def dislike(request, snack_id):
    snack= Snack.objects.get(id= snack_id)
    user= User.objects.get(id= request.session['user_id'])
    snack.disliked_by.add(user)
    snack.liked_by.remove(user)
    return redirect(f'/snacks/{snack.id}')