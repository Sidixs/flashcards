from django.shortcuts import render

from Fiszki.models import SetOfFlashcards


def home(request):
    zestawyFiszek = SetOfFlashcards.objects.all()
    return render(request, 'home.html', {'zestawyFiszek':zestawyFiszek})