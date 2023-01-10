from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

from Fiszki.models import SetOfFlashcards, Flashcards


def flashcard(request, zestFiszId):
    setOfFlashcards = SetOfFlashcards.objects.get(id = zestFiszId)
    flashcards_list = Flashcards.objects.filter(set_of_flashcards=zestFiszId)
    page = request.GET.get('page', 1)
    paginator = Paginator(flashcards_list, 1)
    try:
        flashcards = paginator.page(page)
    except PageNotAnInteger:
        flashcards = paginator.page(1)
    except EmptyPage:
        flashcards = paginator.page(paginator.num_pages)
    context= {'setOfFlashcards':setOfFlashcards, 'flashcards':flashcards}

    return render(request, 'flashcard.html', context)