from django.shortcuts import render, redirect

from Fiszki.models import SetOfFlashcards


def flashcards(request):
    SetOfCards = SetOfFlashcards.objects.all()
    if request.method == "POST":
        if "delete-card-id" in request.POST:
            cardId =request.POST.get("delete-card-id")
            card = SetOfFlashcards.objects.filter(id = cardId).first()
            if card and request.user.is_superuser:
                card.delete()
                return redirect('manage-flashcards')
        if "edit-card-id" in request.POST:
            return redirect()
    return render(request, 'manage-flashcards.html', {'SetOfCards':SetOfCards})