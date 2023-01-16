from django.shortcuts import render, redirect

from Fiszki.forms import SetOfFlashcardsForm, FlashcardsForm
from Fiszki.models import SetOfFlashcards, Flashcards


def setsOfFlashcards(request):
    SetOfCards = SetOfFlashcards.objects.all()
    SetOfCardsForm = SetOfFlashcardsForm()
    if request.method == "POST":
        if 'add-card-set' in request.POST:
            SetOfCardsForm = SetOfFlashcardsForm(request.POST)
            if SetOfCardsForm.is_valid():
                SetOfCardsForm.save()
                return redirect('manage-flashcards')

        if 'delete-card-set-id' in request.POST:
            cardSetId =request.POST.get("delete-card-set-id")
            cardSet = SetOfFlashcards.objects.filter(id = cardSetId).first()
            if cardSet and request.user.is_superuser:
                cardSet.delete()
                return redirect('manage-flashcards')
    return render(request, 'manage-flashcards.html', {'SetOfCards':SetOfCards,'SetOfCardsForm':SetOfCardsForm})

def flashcardDetails(request, SOFId):
    # print("ASD"+SOFId)
    cardForm = FlashcardsForm()
    setOfFlashcards = SetOfFlashcards.objects.get(id=SOFId)
    flashcards = Flashcards.objects.filter(set_of_flashcards=SOFId)
    context = {'setOfFlashcards': setOfFlashcards, 'flashcards': flashcards,'cardForm':cardForm}
    if request.method == "POST":
        # a = Flashcards(set_of_flashcards_id=SOFId,first="fsdafdvcxzvcxz",second="adsafdsafds")
        # a.save()
        if 'add-card' in request.POST:
            cardForm = FlashcardsForm(request.POST)
            if cardForm.is_valid():
                card = cardForm.save(commit=False)
                card.set_of_flashcards_id = SOFId
                card.save()
                return redirect('manage-flashcard', SOFId=SOFId)

        if 'delete-card-id' in request.POST:
            cardId = request.POST.get('delete-card-id')
            card = Flashcards.objects.filter(id = cardId).first()
            if card and request.user.is_superuser:
                card.delete()
                return redirect('manage-flashcard', SOFId=SOFId)
    return render(request, 'manage-flashcard.html', context)