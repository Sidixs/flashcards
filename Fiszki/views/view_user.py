from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

from Fiszki.models import SetOfUserFlashcards, AuthUser


def profile(request, userId):
    # if request.method == "POST":
    #     if 'add-card' in request.POST:
    #         cardForm = UserFlashcardsForm(request.POST)
    #         if cardForm.is_valid():
    #             card = cardForm.save(commit=False)
    #             card.set_of_user_flashcards_id = SOUFId
    #             card.save()
    #             return redirect('user-manage-flashcard', SOUFId=SOUFId)
    #     if 'delete-card-id' in request.POST:
    #         cardId = request.POST.get('delete-card-id')
    #         card = UserFlashcards.objects.filter(id = cardId).first()
    #         if card and request.user.is_authenticated:
    #             card.delete()
    #             return redirect('user-manage-flashcard', SOUFId=SOUFId)
    #     if 'edit-card-set-name' in request.POST:
    #         cardSetForm = SetOfUserFlashcardsForm(request.POST)
    #         if cardSetForm.is_valid() and request.user.is_authenticated:
    #             SetOfUserFlashcards.objects.filter(id=SOUFId).update(name=cardSetForm.cleaned_data['name'])
    #             SetOfUserFlashcards.objects.filter(id=SOUFId).update(is_private=cardSetForm.cleaned_data['is_private'])
    #             return redirect('user-manage-flashcard', SOUFId=SOUFId)
    if userId == request.user.id:
        # print("tete")
        setOfProfileFlashcardsList = SetOfUserFlashcards.objects.filter(auth_user_id=userId)
    else:
        setOfProfileFlashcardsList = SetOfUserFlashcards.objects.filter(auth_user_id=userId, is_private=False)
    page = request.GET.get('page', 1)
    paginator = Paginator(setOfProfileFlashcardsList, 5)
    try:
        setOfProfileFlashcards = paginator.page(page)
        # for i in SetOfUserCards:
        #     i.new = SetOfUserCards.filter(userfavorite__auth_user=request.user.id,
        #                         userfavorite__set_of_user_flashcards=i.id).exists()
    except PageNotAnInteger:
        setOfProfileFlashcards = paginator.page(1)
    except EmptyPage:
        setOfProfileFlashcards = paginator.page(paginator.num_pages)

    try:
        profile = AuthUser.objects.get(id=userId)
    except ObjectDoesNotExist:
        profile = None
    context = {'setOfProfileFlashcards': setOfProfileFlashcards,'profile':profile}
    # setOfProfileFlashcardsList.auth_user.username
    return render(request, 'profile.html', context)