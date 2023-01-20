from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

from Fiszki.models import SetOfUserFlashcards, UserFlashcards


def userFlashcards(request):
    SetOfUserCards = SetOfUserFlashcards.objects.filter(is_private=False)
    return render(request, 'user-flashcards.html', {'SetOfUserCards':SetOfUserCards})

def userFlashcard(request, SOUFId):
    setOfUserFlashcards = SetOfUserFlashcards.objects.get(id = SOUFId)
    flashcards_list = UserFlashcards.objects.filter(set_of_user_flashcards=SOUFId)
    page = request.GET.get('page', 1)
    paginator = Paginator(flashcards_list, 1)
    try:
        flashcards = paginator.page(page)
    except PageNotAnInteger:
        flashcards = paginator.page(1)
    except EmptyPage:
        flashcards = paginator.page(paginator.num_pages)
    context= {'setOfUserFlashcards':setOfUserFlashcards, 'flashcards':flashcards}

    return render(request, 'user-flashcard.html', context)