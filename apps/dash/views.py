from django.shortcuts import render, redirect
from .models import *
from apps.login.models import *
from django.contrib import messages


def dashboard(request):
    if 'logged_user' in request.session:
        
        context = {
            'thoughts': Thought.objects.all(),
            'user': User.objects.get(id=request.session['logged_id']),
            'users': User.objects.all(),
            'likes': Like.objects.all(),
            'user_likes': Like.objects.filter(owner=User.objects.get(id=request.session['logged_id']))            
        }
        return render(request, 'dash.html', context)
    return redirect('/')
    



def make_thought(request):
    post = request.POST['title']
    errors = {}
        # agregue claves y valores al diccionario de errores para cada campo no válido
    if len(post) < 5:
        errors["title1"] = "El pensamiento debe tener al menos 5 caracteres"
    elif len(post) == '':
        errors["title2"] = "El campo no debe estar vacío"
    if len(errors) >0:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect('/thoughts')
    else:
        if request.method == 'POST':
            Thought.objects.create(
                title = request.POST['title'],
                poster = User.objects.get(id=request.session['logged_id'])
            )
        return redirect('/thoughts/')
    
    
def detail(request, tid):
    thought = Thought.objects.get(id=tid)
    likes = thought.likes.all()
    tot_likes = thought.likes.all().count()
    owner = User.objects.get(id=request.session['logged_id'])
    liked=False
    for like in likes:
        if owner.id is like.owner.id:
            liked=True
    context = {
        'thought':thought,
        'likes':likes,
        'already_liked': liked,
        'tot_likes': tot_likes
        }
    return render(request, 'detail.html', context)

def like(request, tid):
    thought = Thought.objects.get(id=tid)
    owner = User.objects.get(id=request.session['logged_id'])
    already_liked=False

    for like in thought.likes.all():
        if owner.id is like.owner.id:
            already_liked=True
    if already_liked:
        return redirect(f'/thoughts/{tid}')
    Like.objects.create(
            thought = Thought.objects.get(id=tid),
            owner = User.objects.get(id=request.session['logged_id'])
        )
    return redirect(f'/thoughts/{tid}')

def dislike(request, tid):
    thought = Thought.objects.get(id=tid)
    owner = User.objects.get(id=request.session['logged_id'])
    already_liked=False

    for like in thought.likes.all():
        if owner.id is like.owner.id:
            already_liked=True
    if already_liked:
        rem_like = Like.objects.filter(owner=owner.id).filter(thought=thought.id)
        rem_like.delete()
    return redirect(f'/thoughts/{tid}')

def delete(request, tid):
    rem_thought = Thought.objects.get(id=tid)
    rem_thought.delete()
    return redirect('/thoughts')
        