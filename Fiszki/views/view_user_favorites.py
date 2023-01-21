from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect

from Fiszki.models import SetOfUserFlashcards, UserFavorite


def userFavorites(request):
    if request.method == "POST":
        if 'delete-from-favorite' in request.POST:
            favId = request.POST.get('delete-from-favorite')
            favCard = UserFavorite.objects.filter(set_of_user_flashcards_id=favId,auth_user_id=request.user.id).first()
            if favCard and request.user.is_authenticated:
                favCard.delete()
                page = request.GET.get('page', 1)
                response = redirect('user-favorites')
                response['Location'] += "?page=" + str(page)
                return response
    favorites = UserFavorite.objects.filter(auth_user_id=request.user.id)
    SetOfUserCardsList = SetOfUserFlashcards.objects.filter(is_private=False, id__in=favorites.values('set_of_user_flashcards_id'))
    page = request.GET.get('page', 1)
    paginator = Paginator(SetOfUserCardsList, 5)
    try:
        SetOfUserCards = paginator.page(page)
    except PageNotAnInteger:
        SetOfUserCards = paginator.page(1)
    except EmptyPage:
        SetOfUserCards = paginator.page(paginator.num_pages)
    return render(request, 'user-favorites.html', {'SetOfUserCards':SetOfUserCards})