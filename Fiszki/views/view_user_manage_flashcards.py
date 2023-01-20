from django.shortcuts import redirect, render

from Fiszki.forms import SetOfUserFlashcardsForm, UserFlashcardsForm
from Fiszki.models import UserFlashcards, SetOfUserFlashcards


def setsOfUserFlashcards(request):
    if request.method == "POST":
        if 'add-card-set' in request.POST:
            SetOfCardsForm = SetOfUserFlashcardsForm(request.POST)
            if SetOfCardsForm.is_valid():
                #SetOfCardsForm.auth_user_id = request.user.id
                Set = SetOfCardsForm.save(commit=False)
                Set.auth_user_id = request.user.id
                Set.save()
                return redirect('user-manage-flashcards')

        if 'delete-card-set-id' in request.POST:
            cardSetId =request.POST.get("delete-card-set-id")
            # print(cardSetId)
            cardSet = SetOfUserFlashcards.objects.filter(id = cardSetId).first()
            # print(cardSet.id)
            # print(request.user.is_authenticated)
            if cardSet and request.user.is_authenticated and cardSet.auth_user_id == request.user.id:
                UserFlashcards.objects.filter(set_of_user_flashcards=cardSetId).delete()
                cardSet.delete()
                return redirect('user-manage-flashcards')
    SetOfCards = SetOfUserFlashcards.objects.filter(auth_user_id=request.user.id)
    #print(SetOfCards)
    SetOfCardsForm = SetOfUserFlashcardsForm()
    return render(request, 'user-manage-flashcards.html', {'SetOfCards':SetOfCards,'SetOfCardsForm':SetOfCardsForm})

def userFlashcardDetails(request, SOUFId):
    if request.method == "POST":
        if 'add-card' in request.POST:
            cardForm = UserFlashcardsForm(request.POST)
            if cardForm.is_valid():
                card = cardForm.save(commit=False)
                card.set_of_user_flashcards_id = SOUFId
                card.save()
                return redirect('user-manage-flashcard', SOUFId=SOUFId)
        if 'delete-card-id' in request.POST:
            cardId = request.POST.get('delete-card-id')
            card = UserFlashcards.objects.filter(id = cardId).first()
            if card and request.user.is_authenticated:
                card.delete()
                return redirect('user-manage-flashcard', SOUFId=SOUFId)
        if 'edit-card-set-name' in request.POST:
            cardSetForm = SetOfUserFlashcardsForm(request.POST)
            if cardSetForm.is_valid() and request.user.is_authenticated:
                SetOfUserFlashcards.objects.filter(id=SOUFId).update(name=cardSetForm.cleaned_data['name'])
                SetOfUserFlashcards.objects.filter(id=SOUFId).update(is_private=cardSetForm.cleaned_data['is_private'])
                return redirect('user-manage-flashcard', SOUFId=SOUFId)
    cardForm = UserFlashcardsForm()
    setOfFlashcards = SetOfUserFlashcards.objects.get(id=SOUFId)
    setOfFlashcardsForm = SetOfUserFlashcardsForm()
    setOfFlashcardsForm.fields['name'].initial = setOfFlashcards.name
    setOfFlashcardsForm.fields['is_private'].initial = setOfFlashcards.is_private
    flashcards = UserFlashcards.objects.filter(set_of_user_flashcards=SOUFId)
    context = {'setOfFlashcards': setOfFlashcards, 'flashcards': flashcards, 'cardForm': cardForm,
               'setOfFlashcardsForm': setOfFlashcardsForm}
    return render(request, 'user-manage-flashcard.html', context)

def userFlashcardEdit(request, SOUFId, cardId):
    if request.method == "POST":
        if 'edit-card' in request.POST:
            cardForm = UserFlashcardsForm(request.POST)
            if cardForm.is_valid():
                UserFlashcards.objects.filter(id=cardId).update(first=cardForm.cleaned_data['first'], second=cardForm.cleaned_data['second'])
                return redirect('user-manage-flashcard', SOUFId=SOUFId)

    cardForm = UserFlashcardsForm()
    setOfFlashcards = SetOfUserFlashcards.objects.get(id=SOUFId)
    card = UserFlashcards.objects.filter(id=cardId).first()
    cardForm.fields['first'].initial = card.first
    cardForm.fields['second'].initial = card.second
    context = {'setOfFlashcards': setOfFlashcards, 'cardForm': cardForm}
    return render(request, 'user-edit-flashcard.html', context)