from datetime import datetime, timedelta

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect

from Fiszki.models import AuthUser, Ban


def manageUsers(request):
    if request.method == "POST":
        if 'ban-week' in request.POST:
            userId = request.POST.get("ban-week")
            if Ban.objects.filter(auth_user_id=userId).exists():
                Ban.objects.filter(auth_user_id=userId).update(ban_to=datetime.now() + timedelta(days=7))
            else:
                Ban(auth_user_id=userId,ban_to=datetime.now() + timedelta(days=7)).save()
            return redirect('manage-users')
        if 'ban-month' in request.POST:
            userId = request.POST.get("ban-month")
            print("das")
            if Ban.objects.filter(auth_user_id=userId).exists():
                Ban.objects.filter(auth_user_id=userId).update(ban_to=datetime.now() + timedelta(days=30))
            else:
                Ban(auth_user_id=userId,ban_to=datetime.now() + timedelta(days=30)).save()
            return redirect('manage-users')
        if 'ban-perm' in request.POST:
            userId = request.POST.get("ban-perm")
            AuthUser.objects.filter(id=userId).update(is_active=0)
            if Ban.objects.filter(auth_user_id=userId).exists():
                Ban.objects.filter(auth_user_id=userId).update(auth_user_id=userId,
                                                               ban_to=datetime(2099,12,31))
            else:
                Ban(auth_user_id=userId,ban_to=datetime(2099,12,31)).save()
            return redirect('manage-users')
    now = datetime.now()
    usersList = AuthUser.objects.filter(is_superuser=False).order_by('-username')
    b = usersList
    if request.user.is_authenticated:
        for i in usersList:
            i.banList = usersList.filter(id=i.id).values('ban__ban_to')[0]
    page = request.GET.get('page', 1)
    paginator = Paginator(usersList, 5)
    try:
        normalUsers = paginator.page(page)
    except PageNotAnInteger:
        normalUsers = paginator.page(1)
    except EmptyPage:
        normalUsers = paginator.page(paginator.num_pages)
    return render(request, 'manage-users.html', {'normalUsers':normalUsers,'now':now})

def banInfo(request):
    if request.user.is_authenticated and Ban.objects.filter(auth_user=request.user.id).exists():
        banTime = Ban.objects.filter(auth_user=request.user.id).values('ban_to')[0]
    else:
        banTime = None
    now = datetime.now()
    return render(request, 'ban-info.html', {'banTime': banTime,'now':now})