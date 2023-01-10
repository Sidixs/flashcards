from django.shortcuts import render

from Fiszki.models import SetOfFlashcards


def home(request):
    SetOfCards = SetOfFlashcards.objects.all()
    return render(request, 'home.html', {'SetOfCards':SetOfCards})