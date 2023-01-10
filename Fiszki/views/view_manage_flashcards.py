from django.shortcuts import render, redirect

from Fiszki.models import SetOfFlashcards, Flashcards


def setsOfFlashcards(request):
    SetOfCards = SetOfFlashcards.objects.all()
    if request.method == "POST":
        cardSetId =request.POST.get("delete-card-set-id")
        cardSet = SetOfFlashcards.objects.filter(id = cardSetId).first()
        if cardSet and request.user.is_superuser:
            cardSet.delete()
            return redirect('manage-flashcards')
    return render(request, 'manage-flashcards.html', {'SetOfCards':SetOfCards})

def flashcardDetails(request, SOFId):
    print(SOFId)
    setOfFlashcards = SetOfFlashcards.objects.get(id=SOFId)
    flashcards = Flashcards.objects.filter(set_of_flashcards=SOFId)
    context = {'setOfFlashcards': setOfFlashcards, 'flashcards': flashcards}
    if request.method == "POST":
        cardId = request.POST.get('delete-card-id')
        card = Flashcards.objects.filter(id = cardId).first()
        if card and request.user.is_superuser:
            card.delete()
            return redirect('manage-flashcard', SOFId=SOFId)
    return render(request, 'manage-flashcard.html', context)