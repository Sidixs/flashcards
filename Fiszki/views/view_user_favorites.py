from django.shortcuts import render

from Fiszki.models import SetOfUserFlashcards, UserFavorite


def userFavorites(request):
    favorites = UserFavorite.objects.filter(auth_user_id=request.user.id)
    # print(favorites.values_list('set_of_user_flashcards'))
    SetOfUserCards = SetOfUserFlashcards.objects.filter(is_private=False, id__in=favorites.values('set_of_user_flashcards_id'))
    return render(request, 'user-favorites.html', {'SetOfUserCards':SetOfUserCards})