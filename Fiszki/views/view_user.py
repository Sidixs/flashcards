from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect

from Fiszki.models import SetOfUserFlashcards, AuthUser, UserFavorite


def profile(request, userId):
    if request.method == "POST":
        if 'delete-from-favorite' in request.POST:
            favId = request.POST.get('delete-from-favorite')
            favCard = UserFavorite.objects.filter(set_of_user_flashcards_id=favId, auth_user_id=request.user.id).first()
            if favCard and request.user.is_authenticated:
                favCard.delete()
                page = request.GET.get('page', 1)
                response = redirect('profile', userId)
                response['Location'] += "?page=" + str(page)
                return response
                # return redirect('user-flashcards')
        if 'add-to-favorite' in request.POST:
            favId = request.POST.get('add-to-favorite')
            newFavorite = UserFavorite(auth_user_id=request.user.id, set_of_user_flashcards_id=favId, )
            newFavorite.save()
            page = request.GET.get('page', 1)
            response = redirect('profile', userId)
            response['Location'] += "?page=" + str(page)
            return response
    if userId == request.user.id:
        setOfProfileFlashcardsList = SetOfUserFlashcards.objects.filter(auth_user_id=userId)
    else:
        setOfProfileFlashcardsList = SetOfUserFlashcards.objects.filter(is_private=False).exclude(auth_user_id=request.user.id)
        if request.user.is_authenticated:
            for i in setOfProfileFlashcardsList:
                i.Favorite = setOfProfileFlashcardsList.filter(userfavorite__auth_user=request.user.id,
                                                       userfavorite__set_of_user_flashcards=i.id).exists()
    page = request.GET.get('page', 1)
    paginator = Paginator(setOfProfileFlashcardsList, 5)
    try:
        setOfProfileFlashcards = paginator.page(page)
    except PageNotAnInteger:
        setOfProfileFlashcards = paginator.page(1)
    except EmptyPage:
        setOfProfileFlashcards = paginator.page(paginator.num_pages)
    try:
        profile = AuthUser.objects.get(id=userId)
    except ObjectDoesNotExist:
        profile = None
    context = {'setOfProfileFlashcards': setOfProfileFlashcards,'profile':profile}
    return render(request, 'profile.html', context)