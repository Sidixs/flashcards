from django.urls import path

from Fiszki import views

urlpatterns =[
    path('', views.view_home.home, name='home'),
    path('home', views.view_home.home, name='home'),

    path('flashcard/<str:SOFId>', views.view_home.flashcard, name='flashcard'),

    path('user-flashcards', views.view_user_flashcards.userFlashcards, name='user-flashcards'),
    path('user-flashcard/<str:SOUFId>', views.view_user_flashcards.userFlashcard, name='user-flashcard'),

    path('user-favorites', views.view_user_favorites.userFavorites, name='user-favorites'),

    path('manage-users', views.view_manage_users.manageUsers, name='manage-users'),
    path('ban-info', views.view_manage_users.banInfo, name='ban-info'),

    path('manage-flashcards', views.view_manage_flashcards.setsOfFlashcards, name='manage-flashcards'),
    path('manage-flashcard/<str:SOFId>', views.view_manage_flashcards.flashcardDetails, name='manage-flashcard'),
    path('manage-flashcard/<str:SOFId>/<str:cardId>', views.view_manage_flashcards.flashcardEdit, name='edit-flashcard'),

    path('manage-user-flashcards', views.view_manage_user_flashcards.manageUserFlashcards, name='manage-user-flashcards'),
    path('manage-user-flashcards/<str:SOUFId>', views.view_manage_user_flashcards.manageUserFlashcardDetails, name='manage-user-flashcard-details'),

    path('user-manage-flashcards', views.view_user_manage_flashcards.setsOfUserFlashcards, name='user-manage-flashcards'),
    path('user-manage-flashcard/<str:SOUFId>', views.view_user_manage_flashcards.userFlashcardDetails, name='user-manage-flashcard'),
    path('user-manage-flashcard/<str:SOUFId>/<str:cardId>', views.view_user_manage_flashcards.userFlashcardEdit, name='user-edit-flashcard'),

    path('signup', views.view_registration.sign_up, name='signup'),

    path('tos', views.view_site_tos.TOS_page, name='tos'),
    path('profile/<int:userId>', views.view_user.profile, name='profile'),
]