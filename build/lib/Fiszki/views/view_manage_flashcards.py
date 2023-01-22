from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect

from Fiszki.forms import SetOfFlashcardsForm, FlashcardsForm
from Fiszki.models import SetOfFlashcards, Flashcards


def setsOfFlashcards(request):
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
                Flashcards.objects.filter(set_of_flashcards_id=cardSetId).delete()
                cardSet.delete()
                return redirect('manage-flashcards')
    SetOfCardsList = SetOfFlashcards.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(SetOfCardsList, 5)
    try:
        SetOfCards = paginator.page(page)
    except PageNotAnInteger:
        SetOfCards = paginator.page(1)
    except EmptyPage:
        SetOfCards = paginator.page(paginator.num_pages)
    SetOfCardsForm = SetOfFlashcardsForm()
    return render(request, 'manage-flashcards.html', {'SetOfCards':SetOfCards,'SetOfCardsForm':SetOfCardsForm})

def flashcardDetails(request, SOFId):
    if request.method == "POST":
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
        if 'edit-card-set-name' in request.POST:
            cardSetForm = SetOfFlashcardsForm(request.POST)
            if cardSetForm.is_valid() and request.user.is_superuser:
                SetOfFlashcards.objects.filter(id=SOFId).update(name=cardSetForm.cleaned_data['name'])
                return redirect('manage-flashcard', SOFId=SOFId)
    cardForm = FlashcardsForm()
    setOfFlashcards = SetOfFlashcards.objects.get(id=SOFId)
    setOfFlashcardsForm = SetOfFlashcardsForm()
    setOfFlashcardsForm.fields['name'].initial = setOfFlashcards.name
    flashcards = Flashcards.objects.filter(set_of_flashcards=SOFId)
    context = {'setOfFlashcards': setOfFlashcards, 'flashcards': flashcards, 'cardForm': cardForm,
               'setOfFlashcardsForm': setOfFlashcardsForm}
    return render(request, 'manage-flashcard.html', context)

def flashcardEdit(request, SOFId, cardId):
    if request.method == "POST":
        if 'edit-card' in request.POST:
            cardForm = FlashcardsForm(request.POST)
            if cardForm.is_valid():
                Flashcards.objects.filter(id=cardId).update(first=cardForm.cleaned_data['first'], second=cardForm.cleaned_data['second'])
                return redirect('manage-flashcard', SOFId=SOFId)

    cardForm = FlashcardsForm()
    setOfFlashcards = SetOfFlashcards.objects.get(id=SOFId)
    card = Flashcards.objects.filter(id=cardId).first()
    cardForm.fields['first'].initial = card.first
    cardForm.fields['second'].initial = card.second
    context = {'setOfFlashcards': setOfFlashcards, 'cardForm': cardForm}
    return render(request, 'edit-flashcard.html', context)