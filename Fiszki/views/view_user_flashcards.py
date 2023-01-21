from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Subquery, Value, BooleanField, Exists
from django.shortcuts import render, redirect

from Fiszki.models import SetOfUserFlashcards, UserFlashcards, UserFavorite


def userFlashcards(request):
    if request.method == "POST":
        if 'delete-from-favorite' in request.POST:
            favId = request.POST.get('delete-from-favorite')
            favCard = UserFavorite.objects.filter(set_of_user_flashcards_id=favId,auth_user_id=request.user.id).first()
            if favCard and request.user.is_authenticated:
                favCard.delete()
                page = request.GET.get('page', 1)
                response = redirect('user-flashcards')
                response['Location'] += "?page=" + str(page)
                return response
                #return redirect('user-flashcards')
        if 'add-to-favorite' in request.POST:
            favId = request.POST.get('add-to-favorite')
            newFavorite = UserFavorite(auth_user_id=request.user.id, set_of_user_flashcards_id=favId,)
            newFavorite.save()
            page = request.GET.get('page', 1)
            response = redirect('user-flashcards')
            response['Location'] += "?page=" + str(page)
            return response
            #return redirect('user-flashcards')

    SetOfUserCardsList = SetOfUserFlashcards.objects.filter(is_private=False).exclude(auth_user_id=request.user.id)
    # card = SetOfUserCardsList
    if request.user.is_authenticated:
        for i in SetOfUserCardsList:
            i.Favorite=SetOfUserCardsList.filter(userfavorite__auth_user=request.user.id,userfavorite__set_of_user_flashcards=i.id).exists()
    # print(SetOfUserCardsList.filter(userfavorite__auth_user=request.user.id))
    # print(card.values('auth_user__userfavorite__set_of_user_flashcards').count())
    page = request.GET.get('page', 1)
    paginator = Paginator(SetOfUserCardsList, 5)
    try:
        SetOfUserCards = paginator.page(page)
        # for i in SetOfUserCards:
        #     i.new = SetOfUserCards.filter(userfavorite__auth_user=request.user.id,
        #                         userfavorite__set_of_user_flashcards=i.id).exists()
    except PageNotAnInteger:
        SetOfUserCards = paginator.page(1)
    except EmptyPage:
        SetOfUserCards = paginator.page(paginator.num_pages)
    return render(request, 'view-user-flashcards.html', {'SetOfUserCards':SetOfUserCards})

def userFlashcard(request, SOUFId):
    if request.method == "POST":
        if 'add-to-favorite' in request.POST:
            # cardForm = UserFlashcardsForm(request.POST)
            newFavorite = UserFavorite(auth_user_id=request.user.id,set_of_user_flashcards_id=SOUFId)
            newFavorite.save()
            page = request.GET.get('page', 1)
            # print(page)
            response = redirect('user-flashcard', SOUFId=SOUFId)
            response['Location'] += "?page=" + str(page)
            return response
            # return redirect('user-flashcard', SOUFId=SOUFId,page = page)
        if 'delete-from-favorite' in request.POST:
            UserFavorite.objects.filter(auth_user_id=request.user.id, set_of_user_flashcards_id=SOUFId).delete()
            page = request.GET.get('page', 1)
            response = redirect('user-flashcard', SOUFId=SOUFId)
            response['Location'] += "?page=" + str(page)
            return response

    setOfUserFlashcards = SetOfUserFlashcards.objects.get(id = SOUFId)
    isFavorite = UserFavorite.objects.filter(auth_user_id=request.user.id,set_of_user_flashcards_id=SOUFId).exists()
    # print(isFavorite)
    flashcards_list = UserFlashcards.objects.filter(set_of_user_flashcards=SOUFId)
    page = request.GET.get('page', 1)
    paginator = Paginator(flashcards_list, 1)
    try:
        flashcards = paginator.page(page)
    except PageNotAnInteger:
        flashcards = paginator.page(1)
    except EmptyPage:
        flashcards = paginator.page(paginator.num_pages)
    context= {'setOfUserFlashcards':setOfUserFlashcards, 'flashcards':flashcards,'isFavorite':isFavorite}

    return render(request, 'view-user-flashcard.html', context)