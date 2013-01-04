# Create your views here.
import json

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.shortcuts import redirect, render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages

from models import Shirt, ShirtShot
from forms import ShirtForm, ShotForm, ProfileForm

def home(request, query=None, tag=None):
    shirt_form = ShirtForm()
    shot_form = ShotForm()
    shirts = query or Shirt.objects.all()
    return render(request, 'index.html', {'shirts': shirts,
                                          'shot_form': shot_form,
                                          'tag': tag })
def tag_gallery(request, tag):
    query = Shirt.objects.filter(tags__name__in=[tag])
    return home(request, query, tag)

def view_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    profile_form = ProfileForm(instance=user) if request.user == user else None
    rank = (User.objects.count() -
            (User.objects
             .annotate(num_shirts=Count('owns'))
             .order_by('-num_shirts')
             .filter(num_shirts__lt=user.owns.count()).count()))
    return render(request, 'user.html', {'pageuser': user,
                                         'rank': rank,
                                         'count_users': User.objects.count()-1,
                                         'profile_form': profile_form})

@login_required
@require_POST
def edit_user(request):
    profile_form = ProfileForm(request.POST, instance=request.user)
    if profile_form.is_valid():
        profile_form.save()
        messages.success(request, 'Yup, changes made.')
    else:
        messages.error(request, 'Nop, something is wrong.')
    return redirect('view_user', request.user.id)


def view_shirt(request, shirt_id):
    shirt = get_object_or_404(Shirt, pk=shirt_id)
    cover = shirt.shots.all()[0]
    owned = shirt.owned_by.filter(pk=request.user.id).exists()
    shirt_form = ShirtForm(instance=shirt)
    shot_form = ShotForm()
    can_edit = (request.user.is_superuser or request.user == shirt.uploaded_by)
    return render(request, 'shirt.html', {'shirt': shirt,
                                          'cover': cover,
                                          'owned': owned,
                                          'can_edit': can_edit,
                                          'shot_form': shot_form,
                                          'shirt_form': shirt_form})

@login_required
@require_POST
def add_shirt(request, shirt_id=None):
    if shirt_id:
        shirt = get_object_or_404(Shirt, pk=shirt_id)
        if not (request.user.is_superuser or
                shirt.uploaded_by == request.user):
            messages.error(request, 'Yeah whatevah dude, nice try.')
            redirect('view_shirt', shirt.id)
    else:
        shirt = Shirt(uploaded_by=request.user)
        shot = ShirtShot(shirt=shirt, uploaded_by=request.user)
        shot_form = ShotForm(request.POST or None, request.FILES or None,
                             instance=shot)

    shirt_form = ShirtForm(request.POST or None, instance=shirt)
    if ((shirt_form.is_valid() and not shirt_id and shot_form.is_valid()) or
        (shirt_form.is_valid() and shirt_id)):
            shirt_form.save()
            message = 'Yeah, shirt edited!'
            if not shirt_id:
                shot_form.instance.shirt = shirt_form.instance
                shot_form.save()
                message = 'Yeah, shirt added!'
            messages.success(request, message)
    else:
        import pdb
        pdb.set_trace()
        messages.error(request, 'Arrrrgh something went wrong, try again')


    return redirect('view_shirt', shirt.id)


@login_required
@require_POST
def add_shot(request, shirt_id):
    shirt = get_object_or_404(Shirt, pk=shirt_id)
    shot = ShirtShot(shirt=shirt, uploaded_by=request.user)
    shot_form = ShotForm(request.POST or None, request.FILES or None,
                         instance=shot)
    if shot_form.is_valid():
        messages.success(request, 'Yeah, shot added!')
        shot_form.save()
    else:
        messages.error(request, 'Arrrrgh something went wrong, try again.')

    return redirect('view_shirt', shirt_id)

@login_required
def own_shirt(request, shirt_id, add=True):
    shirt = get_object_or_404(Shirt, pk=shirt_id)
    if add:
        shirt.owned_by.add(request.user)
        messages.success(request, 'Woohoo! Shirt added to your collection.')
    else:
        shirt.owned_by.remove(request.user)
        messages.success(request, 'Boo! Shirt removed from your collection.')
    return redirect('view_shirt', shirt_id)
