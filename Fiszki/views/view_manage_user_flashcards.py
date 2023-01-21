from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect

from Fiszki.models import SetOfUserFlashcards, UserFlashcards, UserFavorite


def manageUserFlashcards(request):
    if request.method == "POST":
        if 'delete-card-set-id' in request.POST:
            cardSetId =request.POST.get("delete-card-set-id")
            cardSet = SetOfUserFlashcards.objects.filter(id = cardSetId).first()
            if cardSet and request.user.is_superuser:
                UserFavorite.objects.filter(set_of_user_flashcards_id=cardSetId).delete()
                UserFlashcards.objects.filter(set_of_user_flashcards_id=cardSetId).delete()
                cardSet.delete()
                return redirect('manage-user-flashcards')
    SetOfCardsList = SetOfUserFlashcards.objects.all().order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(SetOfCardsList, 5)
    try:
        SetOfCards = paginator.page(page)
    except PageNotAnInteger:
        SetOfCards = paginator.page(1)
    except EmptyPage:
        SetOfCards = paginator.page(paginator.num_pages)
    return render(request, 'manage-user-flashcards.html', {'SetOfCards':SetOfCards})

def manageUserFlashcardDetails(request, SOUFId):
    if request.method == "POST":
        if 'delete-card-id' in request.POST:
            cardId = request.POST.get('delete-card-id')
            card = UserFlashcards.objects.filter(id = cardId).first()
            if card and request.user.is_superuser:
                card.delete()
                return redirect('manage-user-flashcard-details', SOUFId=SOUFId)
        if 'delete-set-id' in request.POST:
            cardSetId =request.POST.get("delete-set-id")
            cardSet = SetOfUserFlashcards.objects.filter(id = cardSetId).first()
            if cardSet and request.user.is_superuser:
                UserFavorite.objects.filter(set_of_user_flashcards_id=cardSetId).delete()
                UserFlashcards.objects.filter(set_of_user_flashcards_id=cardSetId).delete()
                cardSet.delete()
                return redirect('manage-user-flashcards')
    setOfFlashcards = SetOfUserFlashcards.objects.get(id=SOUFId)
    flashcards = UserFlashcards.objects.filter(set_of_user_flashcards=SOUFId)
    context = {'setOfFlashcards': setOfFlashcards, 'flashcards': flashcards}
    return render(request, 'manage-user-flashcard-details.html', context)